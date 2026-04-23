test:
	cd harness && .venv/bin/python -m unittest discover -s tests -v

benchmark-mock:
	cd harness && .venv/bin/python run_benchmark.py --provider mock --cases all --no-save

live-matrix:
	bash scripts/live_provider_matrix.sh

api:
	cd harness && .venv/bin/python run_api.py

ui-install:
	cd frontend && npm install

ui:
	cd frontend && npm run dev
