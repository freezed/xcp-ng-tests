# Quick start for XCP-ng tests scripts

_⚠️  This is a **user quick start**, for special tests or developer documentation, go to [`README` page](README.md)_

## 📌 Requirements

1. A **_Test Runner_**, <?_ARE_ALL_OS_OK_?> where you’ll run tests from [this repo](https://github.com/xcp-ng/xcp-ng-tests);
1. A **_Test Target_**, an [XCP-ng _host_]( https://docs.xcp-ng.org/installation/install-xcp-ng/), reachable via SSH (with a SSH key, non-interactively);
1. Most of tests needs one or more VM, more host and specific configuration.


## 🦿 _Test Runner_ configuration

* [`python` >= 3.11](https://www.python.org/downloads/)
* [`netcat`](https://nc110.sourceforge.io/)
* this repo cloned, a virtual environment and the dependencies
  ```bash
  git clone git@github.com:xcp-ng/xcp-ng-tests.git && cd xcp-ng-tests
  python3 -m venv .venv && source .venv/bin/activate
  pip install -r requirements/base.txt
  ```
* setup configuration
  ```bash
  cp data.py-dist data.py && ${EDITOR} data.py
  ```

## 🎯 _Test Target_ configuration

* XCP-ng installed, network with internet access
* available via SSH key exchange


## ⚙️ First test !

This test check if the target can download [some text-files](https://github.com/xcp-ng/xcp-ng-tests/blob/master/tests/misc/test_access_links.py#L26)

```python
pytest tests/misc/test_access_links.py --hosts=<TEST_TARGET_IP>
```

And some variations:

- with 2 _Test Targets_:
  ```python
  pytest tests/misc/test_access_links.py --hosts=<TEST_TARGET_IP_A>,<TEST_TARGET_IP_B>
  ```
- decreasing `pytest` CLI logging:
  ```python
  pytest tests/misc/test_access_links.py --hosts=<TEST_TARGET_IP_A>,<TEST_TARGET_IP_B> --log-cli-level=WARNING
  ```
- increasing `pytest` CLI logging:
  ```python
  pytest tests/misc/test_access_links.py --hosts=<TEST_TARGET_IP_A>,<TEST_TARGET_IP_B> --log-cli-level=DEBUG
  ```

## 🚀 You’re go to go !

This is where this _quick-start_ ends.

Feel free to share improvements of this page, keep in mind that it’s purpose is about to stay as minimal as possible 🤏

You can dive into the [`README` page](README.md) or read more detailed [tests](tests/).


## TODO

- Use templates to spown VM instead of setting up a PXE server