.PHONY: serve token predict test-api

PORT ?= 3001
SERVICE ?= src.service:RFClassifierService
BASE_URL ?= http://127.0.0.1:$(PORT)

serve:
	uv run bentoml serve $(SERVICE) --port $(PORT)

token:
	@curl -s -X POST "$(BASE_URL)/login" \
        -H "Content-Type: application/json" \
        -d '{"credentials":{"username":"user123","password":"password123"}}' | jq -r '.token'

predict:
	@token=$$(curl -s -X POST "$(BASE_URL)/login" \
        -H "Content-Type: application/json" \
        -d '{"credentials":{"username":"user123","password":"password123"}}' | jq -r '.token'); \
	curl -s -X POST "$(BASE_URL)/predict" \
        -H "Content-Type: application/json" \
        -H "Authorization: Bearer $$token" \
        -d '{"input_data":{"place":10,"catu":3,"sexe":1,"secu1":0.0,"year_acc":2021,"victim_age":60,"catv":2,"obsm":1,"motor":1,"catr":3,"circ":2,"surf":1,"situ":1,"vma":50,"jour":7,"mois":12,"lum":5,"dep":77,"com":77317,"agg_":2,"int_":1,"atm":0,"col":6,"lat":48.60,"long":2.89,"hour":17,"nb_victim":2,"nb_vehicules":1}}'; \
	echo

test-api: predict
