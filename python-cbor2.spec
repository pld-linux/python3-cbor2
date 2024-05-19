#
# Conditional build:
%bcond_without	doc	# Sphinx documentation
%bcond_without	tests	# unit tests
%bcond_without	python2 # CPython 2.x module
%bcond_without	python3 # CPython 3.x module

Summary:	CBOR (de)serializer with extensive tag support
Summary(pl.UTF-8):	(De)serializer CBOR z obszerną obsługą znaczników
Name:		python-cbor2
# keep 5.2.x here for python2 support
Version:	5.2.0.post1
Release:	1
License:	MIT
Group:		Libraries/Python
#Source0Download: https://pypi.org/simple/cbor2/
Source0:	https://files.pythonhosted.org/packages/source/c/cbor2/cbor2-%{version}.tar.gz
# Source0-md5:	57f0838f52864ce628621da0498f58f4
Patch0:		cbor2-py2.patch
URL:		https://pypi.org/project/cbor2/
%if %{with python2}
BuildRequires:	python-modules >= 1:2.7
BuildRequires:	python-setuptools >= 1:40.7.0
BuildRequires:	python-setuptools_scm >= 1.7.0
%if %{with tests}
BuildRequires:	python-pytest
BuildRequires:	python-pytest-cov
%endif
%endif
%if %{with python3}
BuildRequires:	python3-modules >= 1:3.5
BuildRequires:	python3-setuptools >= 1:40.7.0
BuildRequires:	python3-setuptools_scm >= 1.7.0
BuildRequires:	python3-setuptools_scm < 6
%if %{with tests}
BuildRequires:	python3-pytest
BuildRequires:	python3-pytest-cov
%endif
%endif
BuildRequires:	rpm-pythonprov
BuildRequires:	rpmbuild(macros) >= 1.714
%if %{with doc}
BuildRequires:	python-sphinx_rtd_theme
BuildRequires:	sphinx-pdg-2
%endif
Requires:	python-modules >= 1:2.7
BuildArch:	noarch
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%description
This library provides encoding and decoding for the Concise Binary
Object Representation (CBOR, RFC 7049) serialization format.

%description -l pl.UTF-8
Ta biblioteka zapewnia kodowanie i dekodowanie formatu serializacji
CBOR (Concise Binary Object Representation, RFC 7049).

%package -n python3-cbor2
Summary:	CBOR (de)serializer with extensive tag support
Summary(pl.UTF-8):	(De)serializer CBOR z obszerną obsługą znaczników
Group:		Libraries/Python
Requires:	python3-modules >= 1:3.5

%description -n python3-cbor2
This library provides encoding and decoding for the Concise Binary
Object Representation (CBOR, RFC 7049) serialization format.

%description -n python3-cbor2 -l pl.UTF-8
Ta biblioteka zapewnia kodowanie i dekodowanie formatu serializacji
CBOR (Concise Binary Object Representation, RFC 7049).

%package apidocs
Summary:	API documentation for Python cbor2 module
Summary(pl.UTF-8):	Dokumentacja API modułu Pythona cbor2
Group:		Documentation

%description apidocs
API documentation for Python cbor2 module.

%description apidocs -l pl.UTF-8
Dokumentacja API modułu Pythona cbor2.

%prep
%setup -q -n cbor2-%{version}
%patch0 -p1

%build
# not supported for python2
export CBOR2_BUILD_C_EXTENSION=0
%if %{with python2}
%py_build

%if %{with tests}
PYTEST_DISABLE_PLUGIN_AUTOLOAD=1 \
PYTEST_PLUGINS="pytest_cov.plugin" \
%{__python} -m pytest tests -k 'not test_huge'
%endif
%endif

%if %{with python3}
%py3_build

%if %{with tests}
PYTEST_DISABLE_PLUGIN_AUTOLOAD=1 \
PYTEST_PLUGINS="pytest_cov.plugin" \
%{__python3} -m pytest tests -k 'not test_huge_truncated_bytes and not test_huge_truncated_string'
%endif
%endif

%if %{with doc}
PYTHONPATH=$(pwd) \
sphinx-build-2 docs docs/_build/html
%endif

%install
rm -rf $RPM_BUILD_ROOT

export CBOR2_BUILD_C_EXTENSION=0

%if %{with python2}
%py_install

%py_postclean
%endif

%if %{with python3}
%py3_install
%endif

%clean
rm -rf $RPM_BUILD_ROOT

%if %{with python2}
%files
%defattr(644,root,root,755)
%doc LICENSE.txt README.rst
%{py_sitescriptdir}/cbor2
%{py_sitescriptdir}/cbor2-%{version}-py*.egg-info
%endif

%if %{with python3}
%files -n python3-cbor2
%defattr(644,root,root,755)
%doc LICENSE.txt README.rst
%{py3_sitescriptdir}/cbor2
%{py3_sitescriptdir}/cbor2-%{version}-py*.egg-info
%endif

%if %{with doc}
%files apidocs
%defattr(644,root,root,755)
%doc docs/_build/html/{_static,modules,*.html,*.js}
%endif
