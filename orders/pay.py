from rest_framework.response import Response
from rest_framework import status
from django.shortcuts import redirect
import requests
import json
from .models import Payment, Cart

MERCHANT = '1344b5d4-0048-11e8-94db-005056a205be'
ZP_API_REQUEST = "https://api.zarinpal.com/pg/v4/payment/request.json"
ZP_API_VERIFY = "https://api.zarinpal.com/pg/v4/payment/verify.json"
ZP_API_STARTPAY = "https://zarinpal.com/pg/StartPay/{authority}"
CallbackURL = 'http://127.0.0.1:8000/api/v1/order/pay/verify/'


def send(user, order):
    if order.coupon_code:
        amount = order.get_total_cost(without_discount=True)
    else:
        amount = order.get_total_cost(without_discount=False)
    req_data = {
        "merchant_id": MERCHANT,
        "amount": amount,
        "callback_url": CallbackURL,
        "description": f'تراکنش کاربر {user.id} برای سفارش {order.id}',
        "metadata": {"mobile": user.phone_number, "email": user.email}
    }
    req_header = {"accept": "application/json",
                  "content-type": "application/json"}
    req = requests.post(url=ZP_API_REQUEST, data=json.dumps(req_data), headers=req_header)

    if req.status_code == 500:
        return Response(data={'err': 'خطا در اتصال به درگاه پرداخت'}, status=req.status_code)

    if len(req.json()['errors']) == 0:
        authority = req.json()['data']['authority']
        msg = {
            'url': ZP_API_STARTPAY.format(authority=authority)
        }
        Payment.objects.create(user=user, order=order, amount=amount, authority=authority)
        return Response(data=msg, status=status.HTTP_200_OK)
    else:
        e_code = req.json()['errors']['code']
        e_message = req.json()['errors']['message']
        err = {
            'error_code': e_code,
            'error_msg': e_message,
        }
        return Response(data=err, status=status.HTTP_400_BAD_REQUEST)


def verify(request):
    t_status = request.query_params['Status']
    t_authority = request.query_params['Authority']
    payment = Payment.objects.get(authority=t_authority)
    order = payment.order
    user = payment.user
    if t_status == 'OK':
        req_header = {"accept": "application/json",
                      "content-type": "application/json"}
        req_data = {
            "merchant_id": MERCHANT,
            "amount": payment.amount,
            "authority": t_authority
        }
        req = requests.post(url=ZP_API_VERIFY, data=json.dumps(req_data), headers=req_header)

        if req.status_code == 500:
            return Response(data={'err': 'خطا در اتصال به درگاه پرداخت'}, status=req.status_code)

        if len(req.json()['errors']) == 0:
            t_status = req.json()['data']['code']
            if t_status == 100:
                msg = {
                    'msg': 'تراکنش موفقیت آمیز بود',
                    'tracking_code': str(req.json()['data']['ref_id']),
                }
                payment.status = True
                payment.tracking_code = str(req.json()['data']['ref_id'])
                payment.save()
                order.paid = True
                order.save()
                Cart.objects.get(user=user).delete()
                return Response(data=msg, status=status.HTTP_200_OK)
            elif t_status == 101:
                msg = {
                    'msg': str(req.json()['data']['message']),
                }
                return Response(data=msg, status=status.HTTP_200_OK)
            else:
                msg = {
                    'msg': str(req.json()['data']['message']),
                }
                return Response(data=msg, status=status.HTTP_400_BAD_REQUEST)
        else:
            e_code = req.json()['errors']['code']
            e_message = req.json()['errors']['message']
            err = {
                'error_code': e_code,
                'error_msg': e_message,
            }
        return Response(data=err, status=status.HTTP_400_BAD_REQUEST)
    else:
        msg = {
            'err': 'تراکنش ناموفق بود'
        }
        return Response(data=msg, status=status.HTTP_400_BAD_REQUEST)
