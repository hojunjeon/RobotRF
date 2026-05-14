# Robot Sorting RL

MuJoCo Fetch robot arm reinforcement learning project.

The current project target is `FetchPickAndPlace-v4` from Gymnasium-Robotics. The training path uses Stable-Baselines3 `SAC` with `HerReplayBuffer`, and rollout videos are generated from saved checkpoints.

## Environment Policy

Keep runtime environments separate:

- Windows PowerShell: `.venv-win` for tests, evaluation, and video generation.
- WSL Ubuntu: `/home/ubuntu/.venvs/rrf` for long training.
- Legacy `.venv` and `.venv-wsl` under the repository root are not used.

For a clean setup on another PC, follow [docs/setup_new_machine.md](docs/setup_new_machine.md).

## Windows Setup

Create or repair the Windows environment:

```powershell
& 'C:\Users\SSAFY\AppData\Local\Python\pythoncore-3.14-64\python.exe' -m venv .venv-win
.\.venv-win\Scripts\python.exe -m pip install -e .[dev]
```

Verify:

```powershell
powershell -NoProfile -ExecutionPolicy Bypass -File .\scripts\check_windows_bootstrap.ps1
.\.venv-win\Scripts\python.exe scripts\check_runtime.py
.\.venv-win\Scripts\python.exe -m pytest
```

## WSL Training Setup

The prepared WSL training interpreter is:

```bash
/home/ubuntu/.venvs/rrf/bin/python
```

Verify from Windows PowerShell:

```powershell
wsl -- bash -lc "cd /mnt/c/Users/SSAFY/Desktop/RRF && ~/.venvs/rrf/bin/python scripts/check_runtime.py"
wsl -- bash -lc "cd /mnt/c/Users/SSAFY/Desktop/RRF && ~/.venvs/rrf/bin/python -m pytest tests/test_robotics_training_path.py tests/test_check_runtime_script.py -q"
```

## Train

Start long training in WSL:

```powershell
wsl -- bash -lc "cd /mnt/c/Users/SSAFY/Desktop/RRF && ~/.venvs/rrf/bin/python scripts/train.py --env-id FetchPickAndPlace-v4 --algo sac --total-timesteps 2000000 --seed 42 --output-dir checkpoints/fetch_wsl_2m --tensorboard-log runs/fetch_wsl_2m --checkpoint-interval 500000 --log-interval-steps 10000"
```

This command starts real training. It may take a long time. Early success rate can remain `0.0` because Fetch pick-and-place uses sparse rewards.

Keep this single-env command as the baseline. To use more CPU/GPU capacity with one SAC policy collecting from multiple MuJoCo environments, run the parallel-env variant:

```powershell
wsl -- bash -lc "cd /mnt/c/Users/SSAFY/Desktop/RRF && OMP_NUM_THREADS=1 MKL_NUM_THREADS=1 ~/.venvs/rrf/bin/python scripts/train.py --env-id FetchPickAndPlace-v4 --algo sac --total-timesteps 2000000 --seed 42 --output-dir checkpoints/fetch_wsl_vec6_2m --tensorboard-log runs/fetch_wsl_vec6_2m --n-envs 6 --batch-size 512 --buffer-size 1000000 --gradient-steps -1 --learning-starts 10000 --n-sampled-goal 4 --log-interval-steps 10000 --checkpoint-interval 500000"
```

The parallel command prints timestep progress such as `timesteps: 10000/500000`.

To continue from a saved parallel checkpoint, keep a separate output directory for the extended run and pass `--resume-from`:

```powershell
wsl -- bash -lc "cd /mnt/c/Users/SSAFY/Desktop/RRF && OMP_NUM_THREADS=1 MKL_NUM_THREADS=1 ~/.venvs/rrf/bin/python scripts/train.py --env-id FetchPickAndPlace-v4 --algo sac --total-timesteps 1000000 --seed 42 --output-dir checkpoints/fetch_wsl_vec6_3m --tensorboard-log runs/fetch_wsl_vec6_2m --n-envs 6 --batch-size 512 --buffer-size 1000000 --gradient-steps -1 --learning-starts 10000 --n-sampled-goal 4 --log-interval-steps 10000 --checkpoint-interval 500000 --resume-from checkpoints/fetch_wsl_vec6_2m/FetchPickAndPlace_v4_sac.zip"
```

## Evaluate

After training:

```powershell
wsl -- bash -lc "cd /mnt/c/Users/SSAFY/Desktop/RRF && ~/.venvs/rrf/bin/python scripts/evaluate.py --env-id FetchPickAndPlace-v4 --checkpoint checkpoints/fetch_wsl_2m/FetchPickAndPlace_v4_sac.zip --episodes 100 --output evals/fetch_results.json"
```

The evaluation output includes:

- `episodes`
- `success_rate`
- `mean_reward`
- `mean_episode_length`

Results are appended to `evals/fetch_results.json`.

## Record Video

Generate the rollout video on Windows:

```powershell
.\.venv-win\Scripts\python.exe scripts\record_video.py --env-id FetchPickAndPlace-v4 --checkpoint checkpoints\fetch_wsl_2m\FetchPickAndPlace_v4_sac.zip --output videos\fetch_wsl_2m_rollout.mp4 --max-steps 50
```

## TensorBoard

```powershell
.\.venv-win\Scripts\tensorboard.exe --logdir runs\fetch_wsl_2m
```

Open:

```text
http://localhost:6006
```

For non-specialist explanations of training metrics such as `success_rate`, `ep_rew_mean`, `fps`, and `actor_loss`, see [docs/training_log_guide.md](docs/training_log_guide.md).

Before starting the parallel-env experiment, follow [docs/parallel_training_preparation.md](docs/parallel_training_preparation.md).

## Current Scope

Included:

- MuJoCo/Gymnasium-Robotics Fetch environment loading.
- SAC + HER training.
- Checkpoint save/load.
- JSON evaluation metrics.
- MP4 rollout recording.

Not included:

- Project-local 2D tabletop MVP environment.
- Stage 1/Stage 2 curriculum environment.
- Franka/Panda custom asset integration.
- Gazebo/ROS2 integration.
