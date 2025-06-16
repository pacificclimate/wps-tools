# News / Release Notes

## 2.1.4

_2025 Jun 16_

- Maintenance updates, poetry and python versions [#62](https://github.com/pacificclimate/wps-tools/pull/62)

## 2.1.3

_2025 Apr 3_

- Add local path to URL handler
- Chickadee CI test fixes

## 2.1.2

_2025 Mar 5_

- Compatibility fixes
- Use ubuntu-24.04 runners

## 2.1.1

_2024 May 24_

- Replace instances of `docker-dev03` with `marble-dev01`

## 2.1.0

_2024 May 24_

- Upgrade supported Python versions and change installation tool from `pipenv` to `poetry`

## 2.0.0

_2021 May 19_

- Compatibility fixes
- Add new `R` handling methods

## 1.4.0

_2021 Apr 19_

- Remove `R` code from `output_handling`

## 1.3.1

_2021 Apr 14_

- Update `collect_args` to allow for multiple CSVs in one process

## 1.3.0

_2021 Apr 8_

- Add stream handling to `collect_args`

## 1.2.1

_2021 Mar 25_

- Add flexible installation scenarios for non-`R` birds

## 1.2.0

_2021 Jan 28_

- Add `ProcessError` handling methods

## 1.1.0

_2021 Jan 12_

- Add `csv_handler` to `file_handling.py`

## 1.0.3

_2021 Jan 11_

- Fix metalink call in `auto_construct_outputs`

## 1.0.2

_2021 Jan 6_

- Change`pywps>=4.2.6` and `netCDF4>=1.5.4` to resolve
  compatibility and deprecation issues in birds

## 1.0.1

_2021 Jan 5_

- Fixes io bug with `url_handler` import in `io.py`

## 1.0.0

_2021 Jan 5_

- Reorganize modules into `file_handling.py`,
  `logging.py`, `R.py`, `testing.py` and `io.py`
- Create `output_handling.py` module with the
  functions `nc_to_dataset`, `json_to_dict`,
  `rda_to_vector`, `vector_to_dict`, `txt_to_string`,
  `get_robjects` and `auto_construct_outputs`

## 0.4.1

_2020 Dec 16_

- Fixes io bug with `pywps Format` import

## 0.4.0

_2020 Dec 16_

- Add `get_package`, `load_rdata_to_python` and `save_python_to_rdata` functions
- Add `rda_output` and `vector_name` outputs

## 0.3.1

_2020 Nov 26_

- Update `url_path` with new data storage location

## 0.3.0

_2020 Nov 23_

- Add `url_hanlder` and `collect_args` functions
- Add `common_status_percentages` dictionary object

## 0.2.0

_2020 Oct 28_

- Add notebook url targeting method

## 0.1.3

_2020 Sep 24_

- Add `copy_http_content` function

## 0.1.2

_2020 Aug 12_

- Add `logger` parameter to `log_handler` function

## 0.1.1

_2020 Aug 7_

- Add test suite to test `wps_tools` functions

## 0.1.0

_2020 Jul 23_

- Create wps_tools folder containing `utils.py` modules and `io_objects`
- Add `requirements.txt` and `test_requirements.txt`
- Add `python-ci` and `pypi-publish` for github actions on push
