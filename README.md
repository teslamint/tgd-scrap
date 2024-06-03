# 트게더 작성글 크롤러

[트게더](https://tgd.kr)에 작성한 글을 백업하기 위한 [Scrapy](https://scrapy.org) 스크립트입니다.

## 실행 방법

### Poetry 설치

```bash
# 예) macOS에서 Homebrew로 설치하기
brew install poetry
```

### 리포지터리 복제

```bash
git clone https://github.com/teslamint/tgd-scrap
cd tgd-scrap
```

### 패키지 설치

```bash
poetry install
```

### 트게더 세션 아이디 가져오기

트게더 사이트에 로그인한 후 `tgdsess` 쿠키값을 가져옵니다.

### 스파이더 실행

* 예: JSON 파일로 저장하기

```bash
cd tgd_my
poetry run scrapy crawl my -a tgd_session=[가져온 세션 아이디값] -o [저장할 파일명]:json
```

## FAQ

* 403 에러가 나요.

트게더 사이트에 적용된 [CloudFlare](https://www.cloudflare.com) 방화벽에 의해 일시적으로 차단된 상태입니다. 재시도 설정을 추가했기 때문에 실행된 상태로 두고 기다리면 스크랩됩니다.
