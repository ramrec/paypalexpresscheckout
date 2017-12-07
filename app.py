from flask import Flask, render_template, jsonify, request
import paypalrestsdk

app = Flask(__name__)

paypalrestsdk.configure({
  "mode": "sandbox", # sandbox or live
  "client_id": "AXc2BouxwkRCj1wh3O75Kmtucerg65i8wv7VPRmAxKHoGv3lKTaUqGlb7Kv3hJd9ZMqNHnSq8PcagGNd",
  "client_secret": "EILIjMgmCtQqD0jqwGyCxUCYCckTyeVJYGh8EJaDcywdKAri76E0ZhlBHxQdiFlf6L8Glul_rDGG19mo"
})


@app.route('/')
def index():
    return render_template('index.html')

@app.route('/payment', methods=['POST'])
def payment():

	payment = paypalrestsdk.Payment({
	    "intent": "sale",
	    "payer": {
	        "payment_method": "paypal"},
	    "redirect_urls": {
	        "return_url": "http://localhost:3000/payment/execute",
	        "cancel_url": "http://localhost:3000/"},
	    "transactions": [{
	        "item_list": {
	            "items": [{
	                "name": "item",
	                "sku": "item",
	                "price": "5.00",
	                "currency": "USD",
	                "quantity": 1}]},
	        "amount": {
	            "total": "5.00",
	            "currency": "USD"},
	        "description": "This is the payment transaction description."}]})

	if payment.create():
  		print("Payment created successfully")
	else:
  		print(payment.error)

	return jsonify({'id': payment.id})


@app.route('/execute', methods=['POST'])
def execute():
	success = False
	payment = paypalrestsdk.Payment.find(request.form['paymentID'])

	if payment.execute({'payer_id': request.form['payerID']}):
		print('successful payment execution!')
		success = True
	else:
		print(payment.error)

	return jsonify({'success': success})

if __name__ == '__main__':
    app.run(debug=True)
