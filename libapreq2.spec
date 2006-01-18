%bcond_without	static	# don't build static library
%include	/usr/lib/rpm/macros.perl
%define	apxs	/usr/sbin/apxs
Summary:	Apache Request Library
Summary(pl):	Biblioteka ¿±dañ Apache
Name:		libapreq2
#%define	_devel	03
Version:	2.05
Release:	2
License:	Apache Group
Group:		Libraries
Source0:	http://www.apache.org/dist/httpd/libapreq/%{name}-%{version}-dev.tar.gz
# Source0-md5:	0985e102b6d2bc9c747a56b04a85cba6
URL:		http://httpd.apache.org/apreq/
BuildRequires:	%{apxs}
BuildRequires:	apache >= 2.0.46
BuildRequires:	apache-devel >= 2.0.46
BuildRequires:	apache-mod_perl-devel >= 1.99
BuildRequires:	apr-devel >= 1.0.0
BuildRequires:	autoconf >= 2.53
BuildRequires:	automake
BuildRequires:	perl-ExtUtils-XSBuilder >= 0.23
BuildRequires:	libtool
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%description
libapreq is a safe, standards-compliant, high-performance library used
for parsing HTTP cookies, query-strings and POST data.

Version 2 of libapreq is an improved codebase designed around APR and
Apache-2's input filter API.

%description -l pl
libapreq to bezpieczna, zgodna ze standardami, wysoko wydajna
biblioteka s³u¿±ca do przetwarzania ciasteczek HTTP, ³añcuchów zapytañ
oraz danych POST.

Wersja 2 libapreq to ulepszony kod opracowany na bazie APR i API
filtra wej¶ciowego Apache 2.

%package devel
Summary:	libapreq2 header files
Summary(pl):	Pliki nag³ówkowe libapreq2
Group:		Development/Libraries
Requires:	%{name} = %{version}-%{release}

%description devel
libapreq2 header files.

%description devel -l pl
Pliki nag³ówkowe biblioteki libapreq2.

%package static
Summary:	libapreq2 static library
Summary(pl):	Statyczna biblioteka libapreq2
Group:		Development/Libraries
Requires:	%{name}-devel = %{version}-%{release}

%description static
Static version of libapreq2 library.

%description static -l pl
Statyczna wersja biblioteki libapreq2.

%package -n perl-%{name}
Summary:	Perl APIs for libapreq2 - Apache::Request and Apache::Cookie
Summary(pl):	Perlowe API dla libapreq2 - Apache::Request i Apache::Cookie
Group:		Development/Languages/Perl
Conflicts:	perl-libapreq

%description -n perl-%{name}
Perl APIs for libapreq2 - Apache::Request and Apache::Cookie.

%description -n perl-%{name} -l pl
Perlowe API dla libapreq2 - Apache::Request i Apache::Cookie.

%prep
%setup -q -n %{name}-%{version}-dev

%build
%{__perl} -pi -e "s:apr-config:apr-1-config:g" acinclude.m4 Makefile.PL
%{__perl} -pi -e "s:apu-config:apu-1-config:g" acinclude.m4 Makefile.PL
%{__libtoolize}
%{__aclocal}
%{__autoheader}
%{__autoconf}
%{__automake}
%configure \
	--enable-perl-glue \
	--with-apache2-apxs=%{apxs} \
	%{!?with_static:--disable-static}

%{__make}

cd glue/perl
%{__perl} Makefile.PL \
	INSTALLDIRS=vendor
%{__make} \
	OPTIMIZE="%{rpmcflags}"
cd ../..
# TODO: mod_apreq

%install
rm -rf $RPM_BUILD_ROOT

%{__make} install \
	DESTDIR=$RPM_BUILD_ROOT

%{__make} -C glue/perl install \
	DESTDIR=$RPM_BUILD_ROOT

%clean
rm -rf $RPM_BUILD_ROOT

%post	-p /sbin/ldconfig
%postun	-p /sbin/ldconfig

%files
%defattr(644,root,root,755)
%doc CHANGES README
%attr(755,root,root) %{_libdir}/*.so.*.*

%files devel
%defattr(644,root,root,755)
%attr(755,root,root) %{_libdir}/*.so
%{_libdir}/*.la
%{_includedir}/apreq2
#%{_mandir}/man3/libapreq.3*
#%{_examplesdir}/%{name}-%{version}

%if %{with static}
%files static
%defattr(644,root,root,755)
%{_libdir}/*.a
%endif

%files -n perl-%{name}
%defattr(644,root,root,755)
%{perl_vendorarch}/Apache2/*.pm
%dir %{perl_vendorarch}/APR
%{perl_vendorarch}/APR/*.pm
%dir %{perl_vendorarch}/APR/Request
%{perl_vendorarch}/APR/Request/*

%{perl_vendorarch}/auto/APR/*

# TODO: generate these manually; Makefile.PL (and overall logic) is broken
%{_mandir}/man3/Apache*
%{_mandir}/man3/APR*
