<div align="center">
  <img src="./assets/moru-mark.svg" width="112" alt="Moru logo" />
  <h1>Moru</h1>
  <p><strong>Codex용 작업 실행 플러그인</strong></p>

  [![Skill validation](https://github.com/IncleRepo/moru/actions/workflows/validate.yml/badge.svg)](https://github.com/IncleRepo/moru/actions/workflows/validate.yml)
  [![GitHub stars](https://img.shields.io/github/stars/IncleRepo/moru?style=flat-square)](https://github.com/IncleRepo/moru/stargazers)
  [![Downloads](https://img.shields.io/github/downloads/IncleRepo/moru/total?style=flat-square)](https://github.com/IncleRepo/moru/releases)
  [![License: MIT](https://img.shields.io/badge/license-MIT-111827?style=flat-square)](./LICENSE)
</div>

모루는 여러 단계로 이어지는 요청을 처리하는 Codex 플러그인입니다. 프로젝트 문서와 요청을 먼저 읽고, 작업마다 알맞은 스킬과 도구를 사용합니다. 작업 후에는 변경 내용과 확인 결과를 함께 알려줍니다.

## 모루가 하는 일

- 조사부터 구현, 테스트, 문서 정리까지 이어서 진행합니다.
- 프로젝트 규칙과 참고 문서를 먼저 확인합니다.
- 코딩, 문서, 데이터베이스 등 작업에 맞는 스킬과 도구를 사용합니다.
- 서로 독립적인 작업은 나눠서 동시에 진행할 수 있습니다.
- 끝난 작업과 끝내지 못한 작업을 구분해 알려줍니다.

## 설치

현재 버전은 개인 Marketplace에 등록해 사용할 수 있습니다. 먼저 저장소를 로컬 플러그인 경로에 복제합니다.

```powershell
git clone https://github.com/IncleRepo/moru "$HOME\plugins\moru"
```

Codex에서 `$plugin-creator`를 호출해 개인 Marketplace에 등록합니다.

```text
$plugin-creator Add the existing Moru plugin at ~/plugins/moru to my personal marketplace and validate it.
```

등록이 끝나면 플러그인 화면에서 Moru를 설치하고 새 대화를 시작하세요. 자세한 과정은 [OpenAI 플러그인 문서](https://learn.chatgpt.com/ko-KR/docs/build-plugins)에서 확인할 수 있습니다.

## 사용

요청 앞에 `$moru`를 붙입니다.

```text
$moru 이 저장소의 로그인 실패 원인을 찾고, 수정하고, 관련 테스트까지 실행해줘.
```

```text
$moru 첨부한 요구사항을 기준으로 API를 구현하고 문서도 최신 상태로 맞춰줘.
```

```text
$moru 이 변경사항을 리뷰만 해줘. 코드는 수정하지 마.
```

파일 수정이나 외부 작업을 원하지 않는다면 요청에 함께 적어 주세요. 예를 들어 `리뷰만 하고 파일은 수정하지 마`라고 요청하면 검토만 진행합니다.

## 프로젝트 문서 연결

매번 참고해야 하는 문서가 있다면 프로젝트 루트에 `MORU.md`를 만드세요. 요구사항, 팀 규칙, 참고 자료와 작업 대상의 경로를 한곳에 적어 둘 수 있습니다.

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

필요한 항목만 남겨 사용하면 됩니다. 각 항목에는 문서 본문이 아니라 파일 경로를 적습니다. 비밀번호, 토큰, 개인 키는 넣지 마세요. 전체 예시는 [MORU.template.md](./skills/moru/assets/MORU.template.md)에서 볼 수 있습니다.

## 작업 방식

- 프로젝트의 공식 규칙을 먼저 따릅니다.
- 요청받은 범위 안에서 작업합니다.
- 설치된 전문 스킬과 전용 도구를 우선 사용합니다.
- 코드와 문서는 테스트, 빌드, 렌더링 등 알맞은 방법으로 확인합니다.
- 완료 여부는 `COMPLETE`(완료), `PARTIAL`(일부 완료), `BLOCKED`(진행 불가)로 나눠 보고합니다.

자세한 규칙은 [입력과 문서](./skills/moru/references/input-contract.md), [작업 분배](./skills/moru/references/routing.md), [검증과 완료](./skills/moru/references/quality-contract.md)에 정리되어 있습니다.

## 저장소 구조

```text
moru/
├─ .codex-plugin/
│  └─ plugin.json
├─ assets/
│  └─ moru-mark.svg
├─ evals/
│  ├─ README.md
│  └─ cases.json
├─ skills/
│  └─ moru/
│     ├─ SKILL.md
│     ├─ agents/
│     │  └─ openai.yaml
│     ├─ assets/
│     │  └─ MORU.template.md
│     └─ references/
│        ├─ input-contract.md
│        ├─ routing.md
│        └─ quality-contract.md
├─ scripts/
│  ├─ package_plugin.py
│  ├─ smoke_package.py
│  ├─ validate_evals.py
│  └─ validate_plugin.py
└─ README.md
```

## 개발

```powershell
python scripts/validate_plugin.py .
python scripts/validate_evals.py
python scripts/smoke_package.py .
```

위 명령은 플러그인 구조와 평가 데이터를 검사하고 배포용 ZIP을 만듭니다. 만들어진 ZIP은 임시 폴더에 풀어 한 번 더 확인합니다.

릴리스 전에는 [행동 평가 안내](./evals/README.md)에 따라 실제 동작도 확인합니다.

기여 방법은 [CONTRIBUTING.md](./CONTRIBUTING.md), 문의 방법은 [SUPPORT.md](./SUPPORT.md)를 참고하세요. 보안 문제는 [SECURITY.md](./SECURITY.md)의 비공개 신고 절차를 이용해 주세요. 데이터 처리 범위와 이용 조건은 [PRIVACY.md](./PRIVACY.md), [TERMS.md](./TERMS.md)에 정리되어 있습니다.

## 라이선스

[MIT License](./LICENSE)
