from flask import Blueprint, request, jsonify, redirect, make_response
import stripe
from dotenv import load_dotenv
import os
from services.loginService import getUserFromToken
from services.balanceService import addBalance

load_dotenv()

paymentRouter = Blueprint('paymentHandler', __name__)

DOMAIN = os.getenv('DOMAIN')
SERVER_DOMAIN = os.getenv('SERVER_DOMAIN')

@paymentRouter.route('/create-checkout-session', methods = ['POST'])
def checkoutSession():
    products = {
        50: 'price_1NTOkTKHiStKqqWzMup93HQ1',
          100: 'price_1NTOlVKHiStKqqWzk5E85FoL',
            150: 'price_1NTOmYKHiStKqqWza2xiDmOC'
            }
    request_data = request.get_json()
    try:
        token = request_data.get('token')
        amount = request_data.get('amount')
        stripe.api_key = os.getenv('STRIPE_TEST_KEY')
        checkout_session = stripe.checkout.Session.create(
            line_items=[
                {
                    # Provide the exact Price ID (for example, pr_1234) of the product you want to sell
                    'price': products[amount],
                    'quantity': 1,
                },
            ],
            mode='payment',
            success_url=f"{SERVER_DOMAIN}/success?session_id={{CHECKOUT_SESSION_ID}}&token={token}&amount={amount}",
            cancel_url = DOMAIN + '/checkoutfailed'
        )

        return jsonify({'URL': checkout_session.url})
    
    except stripe.error.AuthenticationError as e:
        return "Authentication Error: " + str(e)
    except stripe.error.InvalidRequestError as e:
        return "Invalid Request Error: " + str(e)
    except stripe.error.APIConnectionError as e:
        return "API Connection Error: " + str(e)
    except Exception as e:
        return str(e)

@paymentRouter.route('/success')
def success():
    session_id = request.args.get('session_id')
    mytoken = request.args.get('token')
    value = request.args.get('amount')
    sessionObj = stripe.checkout.Session.retrieve(session_id)
    if sessionObj.payment_status == 'paid':
        username = getUserFromToken(mytoken)
        result = addBalance(value, username)
        if result == True:
            return redirect(DOMAIN + '/checkoutsuccess')
        
    else:
        return redirect(DOMAIN + '/checkoutfailed')
