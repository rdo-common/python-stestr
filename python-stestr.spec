%global pypi_name stestr
%global with_doc 1

%if 0%{?fedora}
%global with_python3 0
%endif

%global common_desc \
stestr is a fork of the testrepository that concentrates on being a \
dedicated test runner for python projects. The generic abstraction layers \
which enabled testr to work with any subunit emitting runner are gone. \
stestr hard codes python-subunit-isms into how it works.

Name:   python-%{pypi_name}
Version:    0.5.0
Release:    3%{?dist}
Summary:    A test runner runner similar to testrepository

License:    ASL 2.0
URL:    https://pypi.python.org/pypi/stestr
Source0:    https://files.pythonhosted.org/packages/source/s/%{pypi_name}/%{pypi_name}-%{version}.tar.gz
BuildArch:  noarch

%description
%{common_desc}

%package -n    python2-%{pypi_name}
Summary:    A test runner runner similar to testrepository
%{?python_provide:%python_provide python2-%{pypi_name}}

BuildRequires:    python2-devel
BuildRequires:    python-setuptools
BuildRequires:    python-pbr

# Test Requirements
BuildRequires:   python-mock
#BuildRequires:  python-subunit2sql

Requires:   python-pbr
Requires:   python-future
Requires:   python-subunit
Requires:   python-fixtures
Requires:   python-six
Requires:   python-testtools
Requires:   PyYAML
# Requires:   python-subunit2sql

%description -n python2-%{pypi_name}
%{common_desc}

%if %{with python3}
%package -n     python3-%{pypi_name}
Summary:        A test runner runner similar to testrepository
%{?python_provide:%python_provide python3-%{pypi_name}}

BuildRequires:    python3-devel
BuildRequires:    python3-setuptools
BuildRequires:    python3-pbr

# Test Requirements
BuildRequires:    python3-mock
# BuildRequires:  python3-subunit2sql

Requires:   python3-pbr
Requires:   python3-future
Requires:   python3-subunit
Requires:   python3-fixtures
Requires:   python3-six
Requires:   python3-testtools
Requires:   python3-PyYAML
# Requires:   python3-subunit2sql

%description -n python3-%{pypi_name}
%{common_desc}
%endif

%if 0%{?with_doc}
%package -n python-%{pypi_name}-doc
Summary:        stestr documentation

BuildRequires:  python-sphinx

%description -n python-%{pypi_name}-doc
%{common_desc}

It contains the documentation for stestr.
%endif

%prep
%autosetup -n %{pypi_name}-%{version}
# Remove bundled egg-info
rm -rf %{pypi_name}.egg-info
rm -f test-requirements.txt requirements.txt

# Remove pbr>=2.0.0 version as it is required for pike
sed -i 's/pbr>=2.0.0/pbr/g' setup.py

%build
%py2_build

%if %{with python3}
%py3_build
%endif

%if 0%{?with_doc}
# generate html docs
%{__python2} setup.py build_sphinx
# remove the sphinx-build leftovers
rm -rf html/.{doctrees,buildinfo}
%endif

%install
%if %{with python3}
%py3_install
cp %{buildroot}/%{_bindir}/stestr %{buildroot}/%{_bindir}/stestr-3
ln -sf %{_bindir}/stestr-3 %{buildroot}/%{_bindir}/stestr-%{python3_version}
%endif

%py2_install
cp %{buildroot}/%{_bindir}/stestr %{buildroot}/%{_bindir}/stestr-2
ln -sf %{_bindir}/stestr-2 %{buildroot}/%{_bindir}/stestr-%{python2_version}


%check
# Skipping tests as python-subunit2sql is not available
%{__python2} setup.py test ||

%if %{with python3}
%{__python3} setup.py test ||
%endif

%files -n python2-%{pypi_name}
%license LICENSE
%doc README.rst
%{_bindir}/stestr
%{_bindir}/stestr-2
%{_bindir}/stestr-%{python2_version}
%{python2_sitelib}/%{pypi_name}
%{python2_sitelib}/%{pypi_name}-%{version}-py?.?.egg-info

%if %{with python3}
%files -n python3-%{pypi_name}
%license LICENSE
%doc README.rst
%{_bindir}/stestr-3
%{_bindir}/stestr-%{python3_version}
%{python3_sitelib}/%{pypi_name}
%{python3_sitelib}/%{pypi_name}-%{version}-py?.?.egg-info
%endif

%if 0%{?with_doc}
%files -n python-%{pypi_name}-doc
%license LICENSE
%doc doc/build/html
%endif

%changelog
* Tue Aug 01 2017 Chandan Kumar <chkumar246@gmail.com> - 0.5.0-3
- Use sed to remove pbr>=2.0.0 dependency

* Tue Aug 01 2017 Chandan Kumar <chkumar246@gmail.com> - 0.5.0-2
- Fixed rpmlint errors

* Mon Jul 31 2017 Chandan Kumar <chkumar246@gmail.com> - 0.5.0-1
- Initial package.
