.PHONY: install test train-stage1 train-stage2 eval-stage1 record-stage1

install:
	python3 -m pip install --upgrade pip
	python3 -m pip install -r requirements.txt

test:
	python3 -m pytest

train-stage1:
	python3 scripts/train.py --stage 1 --algo sac --total-timesteps 50000

train-stage2:
	python3 scripts/train.py --stage 2 --algo sac --total-timesteps 100000

eval-stage1:
	python3 scripts/evaluate.py --stage 1 --checkpoint checkpoints/stage1_sac.zip --episodes 100

record-stage1:
	python3 scripts/record_video.py --stage 1 --checkpoint checkpoints/stage1_sac.zip --output videos/stage1_rollout.mp4
