function update(data) {
    var buy_amount = document.getElementById('id_buy_amount'),
	rate = document.getElementById('id_rate');

    buy_amount.value = data.buy_amount;
    rate.value = data.rate;
}

function update_currencies(data) {
    var sell_currency = document.getElementById('id_sell_currency'),
	buy_currency = document.getElementById('id_buy_currency');

    data.currencies.forEach(
	function(currency) {
	    var sell_option = document.createElement("option"),
		buy_option = document.createElement("option");

	    sell_option.value = currency;
	    sell_option.text = currency;
	    buy_option.value = currency;
	    buy_option.text = currency;

	    sell_currency.options.add(sell_option);
	    buy_currency.options.add(buy_option);
	}
    );
}

function load_currencies(event) {
    var request = new XMLHttpRequest();

    request.open('GET', '/djangoapp/available-currencies/', true);

    request.onload = function() {
	if (request.status >= 200 && request.status < 400) {
	    var data = JSON.parse(request.responseText);
	    update_currencies(data);
	}
    };
    request.send();
}

function check(event) {
    var sell_currency = document.getElementById('id_sell_currency'),
	buy_currency = document.getElementById('id_buy_currency'),
	sell_amount = document.getElementById('id_sell_amount');

    if (!!sell_currency.value &&
	!!buy_currency.value &&
	!!sell_amount) {

	var request = new XMLHttpRequest(),
	    query = ("sell_currency=" + sell_currency.value + "&" +
		     "buy_currency=" + buy_currency.value + "&" +
		     "sell_amount=" + sell_amount.value);
	request.open('GET', '/djangoapp/quote/?' + query, true);

	request.onload = function() {
	    if (request.status >= 200 && request.status < 400) {
		var data = JSON.parse(request.responseText);
		update(data);
	    }
	};
	request.send();

    }
}


window.addEventListener('load', load_currencies);
