.PHONY: install test train-fetch eval-fetch record-fetch

install:
	python3 -m pip install --upgrade pip
	python3 -m pip install -e .[dev]

test:
	python3 -m pytest

train-fetch:
	python3 scripts/train.py --env-id FetchPickAndPlace-v4 --algo sac --total-timesteps 500000 --output-dir checkpoints/fetch_wsl_500k --tensorboard-log runs/fetch_wsl_500k

eval-fetch:
	python3 scripts/evaluate.py --env-id FetchPickAndPlace-v4 --checkpoint checkpoints/fetch_wsl_500k/FetchPickAndPlace_v4_sac.zip --episodes 100

record-fetch:
	python3 scripts/record_video.py --env-id FetchPickAndPlace-v4 --checkpoint checkpoints/fetch_wsl_500k/FetchPickAndPlace_v4_sac.zip --output videos/fetch_wsl_500k_rollout.mp4 --max-steps 50 --start-delay-seconds 1 --end-delay-seconds 1 --fps 25
