from flask import Blueprint, request, jsonify, redirect, make_response
import stripe
from dotenv import load_dotenv
import os
from services.loginService import getUserFromToken
from services.balanceService import addBalance

load_dotenv()

paymentRouter = Blueprint('paymentHandler', __name__)

DOMAIN = os.getenv('DOMAIN')

@paymentRouter.route('/create-checkout-session', methods = ['POST'])
def checkoutSession():
    request_data = request.get_json()
    try:
        token = request_data.get('token')
        stripe.api_key = os.getenv('STRIPE_TEST_KEY')
        checkout_session = stripe.checkout.Session.create(
            line_items=[
                {
                    # Provide the exact Price ID (for example, pr_1234) of the product you want to sell
                    'price': 'price_1NTOkTKHiStKqqWzMup93HQ1',
                    'quantity': 1,
                },
            ],
            mode='payment',
            success_url=f"{DOMAIN}/success?session_id={{CHECKOUT_SESSION_ID}}&token={token}",
            cancel_url = DOMAIN + '/cancel'
        )
    except stripe.error.AuthenticationError as e:
        return "Authentication Error: " + str(e)
    except stripe.error.InvalidRequestError as e:
        return "Invalid Request Error: " + str(e)
    except stripe.error.APIConnectionError as e:
        return "API Connection Error: " + str(e)
    except Exception as e:
        return str(e)

    #return redirect(checkout_session.url, 302)
    # return redirect(checkout_session.url, 302)
    response = make_response(redirect(checkout_session.url, 302))
    response.headers['Access-Control-Allow-Origin'] = '*'

    return response

@paymentRouter.route('/success')
def success():
    session_id = request.args.get('session_id')
    mytoken = request.args.get('token')
    sessionObj = stripe.checkout.Session.retrieve(session_id)
    if sessionObj.payment_status == 'paid':
        username = getUserFromToken(mytoken)
        addBalance(50.0, username)
        return jsonify({'message': 'payment successful and balance updated'})

@paymentRouter.route('/cancel')
def cancel():
    return 'Session canceled'