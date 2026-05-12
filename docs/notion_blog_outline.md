# Notion Blog Outline

## 제목
MuJoCo 스타일 테이블탑 환경에서 SAC + HER로 분리수거 로봇팔 학습하기

## 문제 정의
- 로봇팔이 테이블 위 물체를 집어 올바른 분리수거 박스에 넣는 태스크
- 2주 MVP에서는 비전 인식이 아니라 type feature 기반 분류로 범위를 제한

## 환경 설계
- Fetch PickAndPlace의 action semantics를 따르는 4차원 action
- GoalEnv 구조: `observation`, `achieved_goal`, `desired_goal`
- Stage 1: 단일 목표 박스
- Stage 2: type별 목표 박스

## 학습 설계
- SAC를 메인 알고리즘으로 사용
- HER replay buffer로 실패 경험을 goal relabeling에 활용
- sparse reward 기반으로 성공 판정을 명확히 유지

## 실험 결과
- TensorBoard 학습 곡선
- 100 에피소드 평가 성공률
- before/middle/after rollout 영상

## 회고와 확장
- TD3/TQC/DDPG/PPO 비교 후보
- 실제 MuJoCo Fetch asset 확장
- 카메라 비전 기반 물체 인식
- 컨베이어 벨트와 Sim2Real
