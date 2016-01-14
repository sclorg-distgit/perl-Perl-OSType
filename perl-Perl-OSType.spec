%{?scl:%scl_package perl-Perl-OSType}
%{!?scl:%global pkg_name %{name}}

Name:		%{?scl_prefix}perl-Perl-OSType
Version:	1.006
Release:	3%{?dist}
Summary:	Map Perl operating system names to generic types
License:	GPL+ or Artistic
Group:		Development/Libraries
URL:		http://search.cpan.org/dist/Perl-OSType/
Source0:	http://search.cpan.org/CPAN/authors/id/D/DA/DAGOLDEN/Perl-OSType-%{version}.tar.gz
Patch1:		Perl-OSType-1.005-old-Test::More.patch
Patch2:		Perl-OSType-1.005-stopwords.patch
BuildRoot:	%{_tmppath}/%{pkg_name}-%{version}-%{release}-root-%(id -nu)
BuildArch:	noarch
# Build
BuildRequires:	%{?scl_prefix}perl(ExtUtils::MakeMaker) >= 6.17
# Module
BuildRequires:	%{?scl_prefix}perl(Exporter)
BuildRequires:	%{?scl_prefix}perl(strict)
BuildRequires:	%{?scl_prefix}perl(warnings)
# Test Suite
BuildRequires:	%{?scl_prefix}perl(blib)
BuildRequires:	%{?scl_prefix}perl(constant)
BuildRequires:	%{?scl_prefix}perl(File::Spec)
BuildRequires:	%{?scl_prefix}perl(File::Spec::Functions)
BuildRequires:	%{?scl_prefix}perl(File::Temp)
BuildRequires:	%{?scl_prefix}perl(IO::Handle)
BuildRequires:	%{?scl_prefix}perl(IPC::Open3)
BuildRequires:	%{?scl_prefix}perl(List::Util)
BuildRequires:	%{?scl_prefix}perl(Test::More)
# Optional tests, not run for this dual-lived module when bootstrapping
# Also not run for EPEL-5/6 builds due to package unavailability
%if !%{defined perl_bootstrap} && 0%{?fedora} && ! 0%{?scl:1}
BuildRequires:	%{?scl_prefix}perl(Perl::Critic::Policy::Lax::ProhibitStringyEval::ExceptForRequire)
BuildRequires:	%{?scl_prefix}perl(Pod::Coverage::TrustPod)
BuildRequires:	%{?scl_prefix}perl(Pod::Wordlist::hanekomu)
BuildRequires:	%{?scl_prefix}perl(Test::CPAN::Meta)
BuildRequires:	%{?scl_prefix}perl(Test::MinimumVersion)
BuildRequires:	%{?scl_prefix}perl(Test::Perl::Critic)
BuildRequires:	%{?scl_prefix}perl(Test::Pod)
BuildRequires:	%{?scl_prefix}perl(Test::Pod::Coverage)
BuildRequires:	%{?scl_prefix}perl(Test::Portability::Files)
BuildRequires:	%{?scl_prefix}perl(Test::Spelling), aspell-en
BuildRequires:	%{?scl_prefix}perl(Test::Version)
%endif
# Runtime
%{?scl:%global perl_version %(scl enable %{scl} 'eval "`perl -V:version`"; echo $version')}
%{!?scl:%global perl_version %(eval "`perl -V:version`"; echo $version)}
Requires:	%{?scl_prefix}perl(:MODULE_COMPAT_%{perl_version})

# Test suite needs patching if we have Test::More < 0.88
%{?scl:%global old_test_more %(scl enable %{scl} "perl -MTest::More -e 'print ((\\$Test::More::VERSION < 0.88) ? 1 : 0)'" 2>/dev/null || echo 0)}
%{!?scl:%global old_test_more %(perl -MTest::More -e 'print ($Test::More::VERSION < 0.88 ? 1 : 0);' 2>/dev/null || echo 0)}


%description
Modules that provide OS-specific behaviors often need to know if the current
operating system matches a more generic type of operating systems. For example,
'linux' is a type of 'Unix' operating system and so is 'freebsd'.

This module provides a mapping between an operating system name as given by $^O
and a more generic type. The initial version is based on the OS type mappings
provided in Module::Build and ExtUtils::CBuilder (thus, Microsoft operating
systems are given the type 'Windows' rather than 'Win32').

%prep
%setup -q -n Perl-OSType-%{version}

# Fix test suite for Test::More < 0.88
%if 00%{old_test_more}
%patch1
%endif

# More stopwords for the spell checker
%patch2

%build
%{?scl:scl enable %{scl} "}
perl Makefile.PL INSTALLDIRS=vendor
%{?scl:"}
%{?scl:scl enable %{scl} "}
make %{?_smp_mflags}
%{?scl:"}

%install
rm -rf %{buildroot}
%{?scl:scl enable %{scl} "}
make pure_install DESTDIR=%{buildroot}
%{?scl:"}
find %{buildroot} -type f -name .packlist -exec rm -f {} \;
find %{buildroot} -depth -type d -exec rmdir {} \; 2>/dev/null
%{_fixperms} %{buildroot}

%check
%{?scl:scl enable %{scl} '}
make test
%{?scl:'}
%if !%{defined perl_bootstrap} && 0%{?fedora} && ! 0%{?scl:1}
%{?scl:scl enable %{scl} '}
LANG=en_US make test TEST_FILES="$(echo $(find xt/ -name '*.t'))"
%{?scl:'}
%endif

%clean
rm -rf %{buildroot}

%files
%doc Changes CONTRIBUTING LICENSE README
%{perl_vendorlib}/Perl/
%{_mandir}/man3/Perl::OSType.3pm*

%changelog
* Tue Feb 11 2014 Jitka Plesnikova <jplesnik@redhat.com> - 1.006-3
- Update getting of %%old_test_more
- Resolves: rhbz#1063206

* Mon Feb 10 2014 Jitka Plesnikova <jplesnik@redhat.com> - 1.006-2
- Get correct value for %%old_test_more on SCL
- Resolves: rhbz#1063206

* Tue Nov 19 2013 Jitka Plesnikova <jplesnik@redhat.com> - 1.006-1
- 1.006 bump

* Wed May 15 2013 Jitka Plesnikova <jplesnik@redhat.com> - 1.003-1
- Merge the latest version from RHEL 7 (1.003-2)

* Wed Feb 13 2013 Jitka Plesnikova <jplesnik@redhat.com> - 1.002-1
- SCL package - initial import
