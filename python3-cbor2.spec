#
# Conditional build:
%bcond_without	doc	# Sphinx documentation
%bcond_without	tests	# unit tests

Summary:	CBOR (de)serializer with extensive tag support
Summary(pl.UTF-8):	(De)serializer CBOR z obszerną obsługą znaczników
Name:		python3-cbor2
Version:	5.6.3
Release:	1
License:	MIT
Group:		Libraries/Python
#Source0Download: https://pypi.org/simple/cbor2/
Source0:	https://files.pythonhosted.org/packages/source/c/cbor2/cbor2-%{version}.tar.gz
# Source0-md5:	6d8e78f7a746c94fcd32ff4ae50e5f0a
URL:		https://pypi.org/project/cbor2/
BuildRequires:	glibc-devel >= 6:2.9
BuildRequires:	python3-modules >= 1:3.8
BuildRequires:	python3-setuptools >= 1:61
BuildRequires:	python3-setuptools_scm >= 6.4
%if %{with tests}
BuildRequires:	python3-pytest
BuildRequires:	python3-pytest-cov
%endif
BuildRequires:	rpm-build >= 4.6
BuildRequires:	rpm-pythonprov
BuildRequires:	rpmbuild(macros) >= 1.714
BuildRequires:	sed >= 4.0
%if %{with doc}
BuildRequires:	python3-packaging
BuildRequires:	python3-sphinx_autodoc_typehints >= 1.2.0
BuildRequires:	python3-sphinx_rtd_theme >= 1.0.0
# >= 1.3.0 when available in PLD
%if "%{py3_ver}" != "3.12"
BuildRequires:	python3-typing_extensions
%endif
BuildRequires:	sphinx-pdg-3 >= 4
# >= 7 when available in PLD
%endif
Requires:	python3-modules >= 1:3.8
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%description
This library provides encoding and decoding for the Concise Binary
Object Representation (CBOR, RFC 7049) serialization format.

%description -l pl.UTF-8
Ta biblioteka zapewnia kodowanie i dekodowanie formatu serializacji
CBOR (Concise Binary Object Representation, RFC 7049).

%package apidocs
Summary:	API documentation for Python cbor2 module
Summary(pl.UTF-8):	Dokumentacja API modułu Pythona cbor2
Group:		Documentation
BuildArch:	noarch

%description apidocs
API documentation for Python cbor2 module.

%description apidocs -l pl.UTF-8
Dokumentacja API modułu Pythona cbor2.

%prep
%setup -q -n cbor2-%{version}

%ifarch x32
# different exception raised
%{__sed} -i -e 's/\(cause_exc_class =\) OverflowError/\1 ValueError/' tests/test_decoder.py
%endif

%build
%py3_build

%if %{with tests}
PYTEST_DISABLE_PLUGIN_AUTOLOAD=1 \
PYTEST_PLUGINS="pytest_cov.plugin" \
%{__python3} -m pytest tests
%endif

%if %{with doc}
PYTHONPATH=$(pwd) \
sphinx-build-3 docs docs/_build/html
%endif

%install
rm -rf $RPM_BUILD_ROOT

%py3_install

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr(644,root,root,755)
%doc LICENSE.txt README.rst
%attr(755,root,root) %{_bindir}/cbor2
%{py3_sitedir}/cbor2
%attr(755,root,root) %{py3_sitedir}/_cbor2.cpython-*.so
%{py3_sitedir}/cbor2-%{version}-py*.egg-info

%if %{with doc}
%files apidocs
%defattr(644,root,root,755)
%doc docs/_build/html/{_static,*.html,*.js}
%endif
