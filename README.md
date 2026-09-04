<div align="center">
  <img src="./assets/moru-mark.svg" width="112" alt="Moru logo" />
  <h1>Moru</h1>
  <p><strong>요청을 끝까지 실행하고, 검증된 하나의 결과로 돌려주는 Codex skill.</strong></p>

  [![Skill validation](https://github.com/IncleRepo/moru/actions/workflows/validate.yml/badge.svg)](https://github.com/IncleRepo/moru/actions/workflows/validate.yml)
  [![GitHub stars](https://img.shields.io/github/stars/IncleRepo/moru?style=flat-square)](https://github.com/IncleRepo/moru/stargazers)
  [![Downloads](https://img.shields.io/github/downloads/IncleRepo/moru/total?style=flat-square)](https://github.com/IncleRepo/moru/releases)
  [![License: MIT](https://img.shields.io/badge/license-MIT-111827?style=flat-square)](./LICENSE)
</div>

Moru(모루)는 모든 분야의 지식을 한 파일에 욱여넣은 만능 프롬프트가 아닙니다. 사용자의 요청을 해석하고, 프로젝트의 기본 문서를 찾고, 필요한 전문 skill과 도구를 선택하고, 작업 결과를 검증해 하나로 통합하는 실행 오케스트레이터입니다.

```text
요청
 └─ Moru
     ├─ 프로젝트 문서와 작업 범위 확인
     ├─ 전문 skill · 도구 · 연결 서비스 선택
     ├─ 독립 작업의 선택적 병렬화
     └─ 결과 검증과 통합
          └─ COMPLETE · PARTIAL · BLOCKED
```

## 이런 때 사용합니다

- 코드 수정, 문서 작성, 외부 도구 작업이 한 요청에 함께 들어 있을 때
- 조사부터 구현, 테스트, 결과 정리까지 한 번에 맡기고 싶을 때
- 프로젝트마다 반복해서 설명하던 정책과 참고 문서를 `MORU.md`로 연결하고 싶을 때
- 여러 작업자를 사용하더라도 최종 판단과 결과는 하나로 받고 싶을 때

한 단계로 끝나는 평범한 질문에는 Moru가 필요하지 않습니다. 전문 작업은 해당 분야의 skill이 담당하고, Moru는 범위·순서·권한·검증·통합을 맡습니다.

## 설치

### Skill Installer

Codex에서 다음과 같이 요청합니다.

```text
$skill-installer install https://github.com/IncleRepo/moru
```

### 직접 설치

사용자 skill 디렉터리에 저장소를 복제합니다.

```powershell
git clone https://github.com/IncleRepo/moru "$HOME\.agents\skills\moru"
```

Codex가 skill을 바로 표시하지 않으면 앱이나 CLI를 다시 시작합니다. 설치 위치와 동작 방식은 [공식 OpenAI skill 문서](https://developers.openai.com/codex/skills)를 따릅니다.

## 사용

요청 앞에 `$moru`를 붙이면 됩니다.

```text
$moru 이 저장소의 로그인 실패 원인을 찾고, 수정하고, 관련 테스트까지 실행해줘.
```

```text
$moru 첨부한 요구사항을 기준으로 API를 구현하고 문서도 최신 상태로 맞춰줘.
```

```text
$moru 이 변경사항을 리뷰만 해줘. 코드는 수정하지 마.
```

마지막 예시처럼 범위를 제한하면 Moru는 그 제한을 유지합니다. 리뷰 요청을 임의로 구현 작업으로 바꾸거나, 로컬 초안을 실제 배포로 간주하지 않습니다.

## 프로젝트 기본 문서 연결

프로젝트 루트에 `MORU.md`를 두면 매번 같은 문서 경로를 설명하지 않아도 됩니다. 형식은 사람이 읽기 쉬운 Markdown이며, 필요한 섹션만 사용합니다.

```markdown
# Moru Project Context

## Targets
- src/
- tests/

## Requirements
- docs/requirements.md

## Policies
- AGENTS.md
- docs/security-policy.md

## References
- docs/examples/

## Excluded
- legacy/
```

Moru는 문서 본문을 skill 내부로 복사하지 않습니다. `MORU.md`에는 경로와 역할만 기록하며, 비밀번호·토큰·개인 키를 넣어서는 안 됩니다. 전체 예시는 [MORU.template.md](./assets/MORU.template.md)에서 확인할 수 있습니다.

## 동작 원칙

- 사용자가 요청한 범위와 권한을 끝까지 보존합니다.
- 프로젝트에 등록된 요구사항·정책·참고 자료를 먼저 찾습니다.
- 전문 능력은 설치된 skill과 목적에 맞는 도구를 우선 사용합니다.
- 병렬화는 작업이 독립적이고 통합 비용보다 이득이 클 때만 사용합니다.
- 파일 생성, 코드 수정, 외부 작업을 실제 결과와 근거로 검증합니다.
- 완료 상태는 `COMPLETE`, `PARTIAL`, `BLOCKED` 중 하나로 명확하게 보고합니다.

세부 계약은 [입력과 문서](./references/input-contract.md), [작업 라우팅](./references/routing.md), [검증과 완료](./references/quality-contract.md)에 나뉘어 있습니다.

## 저장소 구조

```text
moru/
├─ SKILL.md
├─ agents/
│  └─ openai.yaml
├─ assets/
│  ├─ MORU.template.md
│  └─ moru-mark.svg
├─ references/
│  ├─ input-contract.md
│  ├─ routing.md
│  └─ quality-contract.md
├─ scripts/
│  ├─ package_skill.py
│  └─ validate_skill.py
└─ README.md
```

## 개발

```powershell
python scripts/validate_skill.py .
python scripts/package_skill.py .
```

첫 번째 명령은 필수 파일, frontmatter, 로컬 문서 링크, 공개 저장소에 들어가면 안 되는 절대 사용자 경로를 검사합니다. 두 번째 명령은 `dist/moru-<version>.zip`을 생성합니다.

변경 제안은 [CONTRIBUTING.md](./CONTRIBUTING.md)를 확인해 주세요. 보안 문제는 공개 이슈보다 [SECURITY.md](./SECURITY.md)의 비공개 신고 절차를 사용해 주세요.

## 라이선스

[MIT License](./LICENSE)

