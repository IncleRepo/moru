# 변경 기록

Moru의 주요 변경 사항을 기록합니다. 버전은 [Semantic Versioning](https://semver.org/)을 따릅니다.

## [Unreleased]

### 추가

- 내부 실행 명세와 분리된 한국어 사용자 문서
- 설치, 프로젝트 설정, 전문 스킬 연결과 작동 구조 안내

## [0.3.0] - 2026-09-04

### 추가

- `MORU.md`의 `Skills` 항목을 이용한 프로젝트별 전문 스킬 기본 설정
- 전문 스킬의 제작, 설치, 프로젝트 연결 방법을 설명하는 사용 안내
- 프로젝트 스킬 선택 우선순위와 권한 경계를 확인하는 행동 평가

## [0.2.0] - 2026-09-04

### 추가

- Git Marketplace에서 바로 등록할 수 있는 저장소 구조
- `codex plugin marketplace upgrade moru`를 이용한 업데이트 흐름

### 변경

- 설치 가능한 플러그인 파일을 `plugins/moru` 아래로 이동
- README와 패키지 검증 도구를 Marketplace 구조에 맞게 정비

## [0.1.1] - 2026-09-04

### 추가

- 원본 저장소를 변경하지 않는 격리 검증 규칙
- 임시 복제본, 원격 변경 경로 차단, 정리 확인을 검증하는 회귀 평가

## [0.1.0] - 2026-09-04

### 추가

- 요청 범위와 권한을 유지하는 작업 실행 흐름
- `MORU.md`를 이용한 프로젝트 문서 등록
- 직접 실행, 정해진 단계 실행, 동적 작업 분배 방식
- 검증 규칙과 `COMPLETE`, `PARTIAL`, `BLOCKED` 완료 상태
- 개인 Marketplace에서 설치할 수 있는 Codex 플러그인 패키지
- `$moru` 명시 호출과 자동 실행 비활성화
- Moru와 독립적으로 동작하는 전문 스킬 연결 방식
- 양성 사례 5개와 음성 사례 3개로 구성된 행동 회귀 평가
- 배포 ZIP 스모크 테스트
- 개인정보 처리방침, 이용 조건, 지원 문서
- GitHub Actions 기반 검증 및 릴리스 자동화

[Unreleased]: https://github.com/IncleRepo/moru/compare/v0.3.0...HEAD
[0.3.0]: https://github.com/IncleRepo/moru/compare/v0.2.0...v0.3.0
[0.2.0]: https://github.com/IncleRepo/moru/compare/v0.1.1...v0.2.0
[0.1.1]: https://github.com/IncleRepo/moru/compare/v0.1.0...v0.1.1
[0.1.0]: https://github.com/IncleRepo/moru/releases/tag/v0.1.0
