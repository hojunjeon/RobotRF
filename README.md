# Robot Sorting RL

Fetch-style tabletop robot sorting reinforcement learning MVP.

The MVP target is a two-stage curriculum:

1. Stage 1: pick one object and place it into one target box.
2. Stage 2: read the object type from state and place the object into the matching box among three boxes.

The environment follows the Gymnasium-Robotics multi-goal API shape:

- `observation`
- `achieved_goal`
- `desired_goal`
- vectorized `compute_reward()`

The training path uses Stable-Baselines3 `SAC` with `HerReplayBuffer`.

## Simulation Environment

The project-local MVP environment is a Fetch-style tabletop simulator with the same action semantics used by Fetch PickAndPlace:

- action shape: `(4,)`
- `dx`, `dy`, `dz`: end-effector displacement
- `gripper`: open/close control

MVP scene:

- one robot gripper abstraction
- one tabletop workspace
- one object per episode
- one target box in stage 1
- three fixed sorting boxes in stage 2
- randomized object start position
- object type provided in the state, not through camera vision

The implementation is intentionally small so the RL pipeline, GoalEnv contract, HER reward behavior, and portfolio deliverables can be developed before adding heavier MuJoCo asset customization. The dependency set includes `gymnasium-robotics` and `mujoco` so the next step can replace the local kinematic environment with a direct Fetch/MuJoCo subclass once the MVP pipeline is stable.

## Windows Quickstart

The current local smoke-test path is Windows PowerShell with a project-local `.venv`.

Check the bootstrap state:

```powershell
powershell -NoProfile -ExecutionPolicy Bypass -File .\scripts\check_windows_bootstrap.ps1
```

Create or repair the virtual environment:

```powershell
& 'C:\Users\SSAFY\AppData\Local\Python\pythoncore-3.14-64\python.exe' -m venv .venv
.\.venv\Scripts\python.exe -m pip install -e .[dev]
```

Verify the runtime:

```powershell
.\.venv\Scripts\python.exe scripts\check_runtime.py
.\.venv\Scripts\python.exe -m pytest
```

Run the stage 1 smoke training path:

```powershell
.\.venv\Scripts\python.exe scripts\train.py --stage 1 --algo sac --total-timesteps 1000 --output-dir checkpoints\smoke --tensorboard-log runs\smoke
.\.venv\Scripts\python.exe scripts\evaluate.py --stage 1 --checkpoint checkpoints\smoke\stage1_sac.zip --episodes 5
```

The smoke run only proves the training loop, TensorBoard logging, checkpoint save, and checkpoint load path. It is not expected to reach a useful success rate.

## WSL2 Quickstart

Use WSL2 Ubuntu 22.04 for longer training runs if Windows file I/O or rendering becomes a bottleneck.

If you are starting from Windows, run the bootstrap check first:

```powershell
powershell -NoProfile -ExecutionPolicy Bypass -File .\scripts\check_windows_bootstrap.ps1
```

From Windows PowerShell:

```powershell
wsl --install -d Ubuntu-22.04
wsl
```

Inside Ubuntu:

```bash
sudo apt update
sudo apt install -y python3 python3-venv python3-pip ffmpeg
mkdir -p ~/projects
cd ~/projects
```

Place or clone this repository under `~/projects/robot-sorting-rl`. Avoid running long training jobs from `/mnt/c/...`; WSL-native paths have more reliable file I/O for logs and checkpoints.

Create the Python environment:

```bash
cd ~/projects/robot-sorting-rl
python3 -m venv .venv
source .venv/bin/activate
make install
```

Check CUDA/PyTorch and MuJoCo imports:

```bash
python3 scripts/check_runtime.py
```

## Commands

Run tests:

```bash
make test
```

Train stage 1:

```bash
make train-stage1
```

Train stage 2:

```bash
make train-stage2
```

Evaluate:

```bash
python3 scripts/evaluate.py --stage 1 --checkpoint checkpoints/stage1_sac.zip --episodes 100
```

Record video:

```bash
python3 scripts/record_video.py --stage 1 --checkpoint checkpoints/stage1_sac.zip --output videos/stage1_rollout.mp4
```

## Algorithm Scope

MVP execution target:

- `SAC + HER`

Documented extension candidates:

- `TD3 + HER`: strongest next comparison for continuous control.
- `TQC + HER`: performance-oriented SB3-Contrib candidate.
- `DDPG + HER`: classic baseline, more tuning-sensitive.
- `PPO`: HER-free on-policy baseline.
- `DQN / QR-DQN`: discrete-action experiment only; not a direct fit for Fetch-style continuous action space.

## MVP Success Criteria

- Stage 1 evaluation success rate: at least 80% over 100 episodes.
- Stage 2 evaluation success rate: at least 80% over 100 episodes.
- Checkpoints, TensorBoard logs, and before/middle/after videos are generated.
- README and blog material explain the curriculum, GoalEnv design, SAC+HER setup, and extension path.

## Docker

Docker Compose is intentionally not the default MVP path. GPU passthrough, MuJoCo headless rendering, ffmpeg, and WSL2-Docker integration add setup risk. Add Docker only after WSL2-native training and recording are stable.
