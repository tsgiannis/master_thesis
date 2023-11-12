# Change Log

## [1.0.13] 2023-10-07
### Changes

- Update Dependencies
- Silent fallback to SQLite
- CI/CD for Render

## [1.0.12] 2023-05-03
### Changes

- Update Gulp Tooling
- Update SCSS
- Update DOCS

## [1.0.11] 2022-11-13
### Chnages

- ✅ Compatible with [LIVE Deployer](https://appseed.us/go-live/)
  - [Deploy Black Dashboard with Drag & Drop](https://www.youtube.com/watch?v=WhawUr_yoMc) - `video material`

## [1.0.10] 2022-09-19
### Chnages

- Added OAuth via Github
- Improved Auth Pages
  - UI/UX updates (minor)
- Added `HEROKU` support
  - via `Procfile`  

## [1.0.9] 2022-09-09
### Improvements

- `Bump UI version`: v1.0.2
  - `Persistent Dark-mode` via local storage

## [1.0.8] 2022-05-25
### Improvements

- Built with [Black Dashboard Generator](https://appseed.us/generator/black-dashboard/)
  - Timestamp: `2022-05-25 09:44`
- Codebase Improvements
- Assets Management via `.env`
  - `ASSETS_ROOT` variable  

## [1.0.7] 2022-05-20
### Improvements

- Version built with [Black Dashboard Generator](https://appseed.us/generator/black-dashboard/)
- Timestamp: `2022-05-20 15:37`

## [1.0.6] 2022-01-16
### Improvements

- Bump Flask Codebase to [v2stable.0.1](https://github.com/app-generator/boilerplate-code-flask-dashboard/releases)
- Dependencies update (all packages) 
  - Flask==2.0.2 (latest stable version)
  - flask_wtf==1.0.0
  - jinja2==3.0.3
  - flask-restx==0.5.1
- Forms Update:
  - Replace `TextField` (deprecated) with `StringField`

## Unreleased
### Fixes

- 2021-11-08 - `v1.0.6-rc1`
  - ImportError: cannot import name 'TextField' from 'wtforms'
    - Problem caused by `WTForms-3.0.0`
    - Fix: use **WTForms==2.3.3**

## [1.0.5] 2021-11-06
### Improvements

- Bump Codebase: [Flask Dashboard](https://github.com/app-generator/boilerplate-code-flask-dashboard) v2.0.0
  - Dependencies update (all packages) 
    - Flask==2.0.1 (latest stable version)
  - Better Code formatting
  - Improved Files organization
  - Optimize imports
  - Docker Scripts Update
  - Gulp Tooling  (SASS Compilation)

## [1.0.4] 2021-05-16
### Dependencies Update

- Bump Codebase: [Flask Dashboard](https://github.com/app-generator/boilerplate-code-flask-dashboard) v1.0.6
- Freeze used versions in `requirements.txt`
    - jinja2 = 2.11.3

## [1.0.3] 2021-03-18
### Improvements

- Bump Codebase: [Flask Dashboard](https://github.com/app-generator/boilerplate-code-flask-dashboard) v1.0.5
- Freeze used versions in `requirements.txt`
    - flask_sqlalchemy = 2.4.4
    - sqlalchemy = 1.3.23

## [1.0.2] 2021-01-13
### Patch bad migration 

- UI: [Jinja Template Black](https://github.com/app-generator/jinja-black-dashboard) v1.0.1
- Patch Pages - previously loaded from another template

## [1.0.1] 2021-01-13
### Improvements 

- Bump UI: [Jinja Template Black](https://github.com/app-generator/jinja-black-dashboard) v1.0.1
- Bump Codebase: [Flask Dashboard](https://github.com/app-generator/boilerplate-code-flask-dashboard) v1.0.3

## [1.0.0] 2020-02-07
### Initial Release
