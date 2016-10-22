%{?scl:%scl_package perl-Perl-OSType}

# Test suite needs patching if we have Test::More < 0.88
%global old_test_more %(%{?scl:scl enable %{scl} '}perl -MTest::More -e %{?scl:'"}'%{?scl:"'}print (($Test::More::VERSION < 0.88) ? 1 : 0);%{?scl:'"}'%{?scl:"'} 2>/dev/null || echo 0%{?scl:'})

# Select the appropriate system speller
%global speller aspell

Name:		%{?scl_prefix}perl-Perl-OSType
Version:	1.010
Release:	2%{?dist}
Summary:	Map Perl operating system names to generic types
License:	GPL+ or Artistic
Group:		Development/Libraries
URL:		http://search.cpan.org/dist/Perl-OSType/
Source0:	http://search.cpan.org/CPAN/authors/id/D/DA/DAGOLDEN/Perl-OSType-%{version}.tar.gz
Patch1:		Perl-OSType-1.010-old-Test::More.patch
Patch2:		Perl-OSType-1.010-stopwords.patch
BuildRoot:	%{_tmppath}/%{name}-%{version}-%{release}-root-%(id -nu)
BuildArch:	noarch
# Build
BuildRequires:	coreutils
BuildRequires:	findutils
BuildRequires:	make
BuildRequires:	%{?scl_prefix}perl
BuildRequires:	%{?scl_prefix}perl-generators
BuildRequires:	%{?scl_prefix}perl(ExtUtils::MakeMaker) >= 6.17
# Module
BuildRequires:	%{?scl_prefix}perl(Exporter)
BuildRequires:	%{?scl_prefix}perl(strict)
BuildRequires:	%{?scl_prefix}perl(warnings)
# Test Suite
BuildRequires:	%{?scl_prefix}perl(blib)
BuildRequires:	%{?scl_prefix}perl(constant)
BuildRequires:	%{?scl_prefix}perl(File::Spec)
BuildRequires:	%{?scl_prefix}perl(Test::More)
# Optional tests, not run for this dual-lived module when bootstrapping
# Also not run for EPEL builds due to package unavailability
%if !%{defined perl_bootstrap} && !%{defined perl_small}
BuildRequires:	%{?scl_prefix}perl(CPAN::Meta) >= 2.120900
BuildRequires:	%{?scl_prefix}perl(CPAN::Meta::Prereqs)
BuildRequires:	%{?scl_prefix}perl(File::Temp)
BuildRequires:	%{?scl_prefix}perl(IO::Handle)
BuildRequires:	%{?scl_prefix}perl(IPC::Open3)
BuildRequires:	%{?scl_prefix}perl(Perl::Critic::Policy::Lax::ProhibitStringyEval::ExceptForRequire)
BuildRequires:	%{?scl_prefix}perl(Pod::Coverage::TrustPod)
BuildRequires:	%{?scl_prefix}perl(Pod::Wordlist)
BuildRequires:	%{?scl_prefix}perl(Test::CPAN::Meta)
BuildRequires:	%{?scl_prefix}perl(Test::MinimumVersion)
BuildRequires:	%{?scl_prefix}perl(Test::Perl::Critic)
BuildRequires:	%{?scl_prefix}perl(Test::Pod) >= 1.41
BuildRequires:	%{?scl_prefix}perl(Test::Pod::Coverage) >= 1.08
BuildRequires:	%{?scl_prefix}perl(Test::Portability::Files)
BuildRequires:	%{?scl_prefix}perl(Test::Spelling), %{speller}-en
BuildRequires:	%{?scl_prefix}perl(Test::Version)
%endif
# Runtime
Requires:	%{?scl_prefix}perl(:MODULE_COMPAT_%(%{?scl:scl enable %{scl} '}eval "$(perl -V:version)";echo $version%{?scl:'}))

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
%if %{old_test_more}
%patch1
%endif

# More stopwords for the spell checker
%patch2

%build
%{?scl:scl enable %{scl} '}perl Makefile.PL INSTALLDIRS=vendor && make %{?_smp_mflags}%{?scl:'}

%install
rm -rf %{buildroot}
%{?scl:scl enable %{scl} '}make pure_install DESTDIR=%{buildroot}%{?scl:'}
find %{buildroot} -type f -name .packlist -delete
%{_fixperms} %{buildroot}

%check
%{?scl:scl enable %{scl} '}make test%{?scl:'}
%if !%{defined perl_bootstrap} && !%{defined perl_small}
LANG=en_US make test TEST_FILES="$(echo $(find xt/ -name '*.t'))"
%endif

%clean
rm -rf %{buildroot}

%files
%if 0%{?_licensedir:1}
%doc LICENSE
%else
%doc LICENSE
%endif
%doc Changes CONTRIBUTING.mkdn README
%{perl_vendorlib}/Perl/
%{_mandir}/man3/Perl::OSType.3*

%changelog
* Mon Jul 11 2016 Petr Pisar <ppisar@redhat.com> - 1.010-2
- SCL

* Wed Jun 22 2016 Paul Howarth <paul@city-fan.org> - 1.010-1
- Update to 1.010
  - Added 'msys' as a Unix-type OS
- BR: perl-generators where available
- Simplify find command using -delete
- Update patches as needed

* Wed May 18 2016 Jitka Plesnikova <jplesnik@redhat.com> - 1.009-366
- Perl 5.24 re-rebuild of bootstrapped packages

* Sat May 14 2016 Jitka Plesnikova <jplesnik@redhat.com> - 1.009-365
- Increase release to favour standalone package

* Thu Feb 04 2016 Fedora Release Engineering <releng@fedoraproject.org> - 1.009-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_24_Mass_Rebuild

* Tue Sep 22 2015 Paul Howarth <paul@city-fan.org> - 1.009-1
- Update to 1.009
  - Added 'sco' as a Unix-type OS
- Update patches as needed

* Thu Jun 18 2015 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.008-347
- Rebuilt for https://fedoraproject.org/wiki/Fedora_23_Mass_Rebuild

* Wed Jun 10 2015 Jitka Plesnikova <jplesnik@redhat.com> - 1.008-346
- Perl 5.22 re-rebuild of bootstrapped packages

* Thu Jun 04 2015 Jitka Plesnikova <jplesnik@redhat.com> - 1.008-345
- Increase release to favour standalone package

* Wed Jun 03 2015 Jitka Plesnikova <jplesnik@redhat.com> - 1.008-2
- Perl 5.22 rebuild

* Fri Jan 30 2015 Paul Howarth <paul@city-fan.org> - 1.008-1
- Update to 1.008
  - Added 'minix' as a Unix-type OS
- Use %%doc where possible
- Update patch for building on old distributions

* Sun Sep 07 2014 Jitka Plesnikova <jplesnik@redhat.com> - 1.007-311
- Perl 5.20 re-rebuild of bootstrapped packages

* Wed Sep 03 2014 Jitka Plesnikova <jplesnik@redhat.com> - 1.007-310
- Increase release to favour standalone package

* Tue Aug 26 2014 Jitka Plesnikova <jplesnik@redhat.com> - 1.007-3
- Perl 5.20 rebuild

* Sat Jun 07 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.007-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_Mass_Rebuild

* Thu Jan 16 2014 Paul Howarth <paul@city-fan.org> - 1.007-1
- Update to 1.007
  - Added 'android' as a Unix-type OS
- Update stopwords patch

* Thu Sep 26 2013 Paul Howarth <paul@city-fan.org> - 1.006-1
- Update to 1.006
  - Compile test could hang on Windows
  - Dropped configure_requires for ExtUtils::MakeMaker to 6.17

* Wed Sep 11 2013 Paul Howarth <paul@city-fan.org> - 1.005-1
- Update to 1.005
  - Ensured no non-core test dependencies
  - Various non-functional changes to files and metadata included with
    the distribution
- Add patch with additional stopwords for the spell checker
- Reinstate EPEL support as we no longer require Capture::Tiny

* Thu Aug 22 2013 Paul Howarth <paul@city-fan.org> - 1.004-1
- Update to 1.004
  - 'bitrig' is a Unix
- Specify all dependencies
- Drop EPEL-5/EPEL-6 support as they don't have Capture::Tiny
- Always use aspell for the spell check as Pod::Wordlist::hanekomu explicitly
  sets the speller to aspell

* Wed Aug 14 2013 Jitka Plesnikova <jplesnik@redhat.com> - 1.003-292
- Perl 5.18 re-rebuild of bootstrapped packages

* Sun Aug 04 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.003-291
- Rebuilt for https://fedoraproject.org/wiki/Fedora_20_Mass_Rebuild

* Mon Jul 15 2013 Petr Pisar <ppisar@redhat.com> - 1.003-290
- Increase release to favour standalone package

* Fri Jul 12 2013 Petr Pisar <ppisar@redhat.com> - 1.003-3
- Perl 5.18 rebuild

* Thu Mar 21 2013 Petr Pisar <ppisar@redhat.com> - 1.003-2
- Disable optional tests on RHEL 7 too

* Thu Mar 21 2013 Paul Howarth <paul@city-fan.org> - 1.003-1
- Update to 1.003
  - Fixed detection of VOS; $^O reports 'vos', not 'VOS'
  - Additional release tests
- BR: perl(File::Spec::Functions), perl(List::Util),
  perl(Perl::Critic::Policy::Lax::ProhibitStringyEval::ExceptForRequire),
  perl(Pod::Wordlist::hanekomu), perl(Test::MinimumVersion),
  perl(Test::Perl::Critic), perl(Test::Spelling) and perl(Test::Version)
- Identify purpose of each build requirement
- Update patches for building on old distributions
- Don't run extra tests for EPEL-5/6 builds

* Thu Feb 14 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.002-242
- Rebuilt for https://fedoraproject.org/wiki/Fedora_19_Mass_Rebuild

* Tue Aug 28 2012 Paul Howarth <paul@city-fan.org> - 1.002-241
- Drop %%defattr, redundant since rpm 4.4
- Don't need to remove empty directories from the buildroot
- Don't delete the extra tests when bootstrapping, but don't run them either

* Fri Aug 17 2012 Petr Pisar <ppisar@redhat.com> - 1.002-240
- Increase release to replace perl sub-package (bug #848961)

* Fri Jul 20 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.002-13
- Rebuilt for https://fedoraproject.org/wiki/Fedora_18_Mass_Rebuild

* Tue Jul 10 2012 Petr Pisar <ppisar@redhat.com> - 1.002-12
- Perl 5.16 re-rebuild of bootstrapped packages

* Wed Jun 06 2012 Petr Pisar <ppisar@redhat.com> - 1.002-11
- Perl 5.16 rebuild

* Fri Jun 01 2012 Petr Pisar <ppisar@redhat.com> - 1.002-10
- Skip author tests on bootstrap

* Thu Jan 12 2012 Paul Howarth <paul@city-fan.org> - 1.002-9
- Fedora 17 mass rebuild

* Wed Aug 17 2011 Paul Howarth <paul@city-fan.org> - 1.002-8
- BR: perl(Pod::Coverage::TrustPod) unconditionally now that it's available in
  EPEL-4

* Tue Aug 16 2011 Marcela Maslanova <mmaslano@redhat.com> - 1.002-7
- Install to vendor perl directories to avoid potential debuginfo conflicts
  with the main perl package if this module ever becomes arch-specific

* Thu Jul 21 2011 Petr Sabata <contyk@redhat.com> - 1.002-6
- Perl mass rebuild

* Tue Jul 19 2011 Petr Sabata <contyk@redhat.com> - 1.002-5
- Perl mass rebuild

* Tue Feb 08 2011 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.002-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_15_Mass_Rebuild

* Wed Jan 26 2011 Paul Howarth <paul@city-fan.org> - 1.002-3
- BR: perl(constant), perl(Exporter), perl(File::Temp) in case they are
  dual-lived at some point (#672801)

* Wed Jan 26 2011 Paul Howarth <paul@city-fan.org> - 1.002-2
- Sanitize for Fedora submission

* Tue Jan 25 2011 Paul Howarth <paul@city-fan.org> - 1.002-1
- Initial RPM version
