#
# Conditional build:
%bcond_without	static_libs	# don't build static library
%bcond_with	tests		# perform "make test"
#
%include	/usr/lib/rpm/macros.perl
%define	apxs	/usr/sbin/apxs
%define	pdir	libapreq2
Summary:	Apache Request Library
Summary(pl.UTF-8):   Biblioteka żądań Apache
Name:		libapreq2
Version:	2.09
Release:	1
License:	Apache 2.0
Group:		Libraries
#Source0:	http://www.apache.org/dist/httpd/libapreq/%{name}-%{version}.tar.gz
Source0:	http://people.apache.org/~pgollucci/apreq2/%{name}-%{version}.tar.gz
# Source0-md5:	3cd98755da8a8431ef35a47461ad67d7
Source1:	apache-mod_apreq2.conf
URL:		http://httpd.apache.org/apreq/
BuildRequires:	%{apxs}
BuildRequires:	apache-devel >= 2.0.46
BuildRequires:	apache-mod_perl-devel >= 1.99
BuildRequires:	apr-devel >= 1.0.0
BuildRequires:	autoconf >= 2.53
BuildRequires:	automake
BuildRequires:	libtool
BuildRequires:	perl-ExtUtils-XSBuilder >= 0.23
%if %{with tests}
BuildRequires:	apache-mod_mime
BuildRequires:	perl-libwww
%endif
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%define		_pkglibdir	%(%{apxs} -q LIBEXECDIR 2>/dev/null)
%define		_sysconfdir	%(%{apxs} -q SYSCONFDIR 2>/dev/null)

%description
libapreq is a safe, standards-compliant, high-performance library used
for parsing HTTP cookies, query-strings and POST data.

Version 2 of libapreq is an improved codebase designed around APR and
Apache-2's input filter API.

%description -l pl.UTF-8
libapreq to bezpieczna, zgodna ze standardami, wysoko wydajna
biblioteka służąca do przetwarzania ciasteczek HTTP, łańcuchów zapytań
oraz danych POST.

Wersja 2 libapreq to ulepszony kod opracowany na bazie APR i API
filtra wejściowego Apache 2.

%package devel
Summary:	libapreq2 header files
Summary(pl.UTF-8):   Pliki nagłówkowe libapreq2
Group:		Development/Libraries
Requires:	%{name} = %{version}-%{release}
Requires:	apache-devel >= 2.0

%description devel
libapreq2 header files.

%description devel -l pl.UTF-8
Pliki nagłówkowe biblioteki libapreq2.

%package static
Summary:	libapreq2 static library
Summary(pl.UTF-8):   Statyczna biblioteka libapreq2
Group:		Development/Libraries
Requires:	%{name}-devel = %{version}-%{release}

%description static
Static version of libapreq2 library.

%description static -l pl.UTF-8
Statyczna wersja biblioteki libapreq2.

%package -n perl-%{name}
Summary:	Perl APIs for libapreq2 - Apache2::Request and Apache2::Cookie
Summary(pl.UTF-8):   Perlowe API dla libapreq2 - Apache2::Request i Apache2::Cookie
Group:		Development/Languages/Perl

%description -n perl-%{name}
Perl APIs for libapreq2 - Apache2::Request and Apache2::Cookie.

%description -n perl-%{name} -l pl.UTF-8
Perlowe API dla libapreq2 - Apache2::Request i Apache2::Cookie.

%package -n apache-mod_apreq2
Summary:	Apache module mod_apreq2
Summary(pl.UTF-8):   Moduł serwera Apache mod_apreq2
Group:		Networking/Daemons
Requires:	apache(modules-api) = %apache_modules_api
Obsoletes:	apache-mod_libapreq2

%description -n apache-mod_apreq2
Apache module mod_apreq2.

%description -n apache-mod_apreq2 -l pl.UTF-8
Moduł mod_apreq2 do serwera Apache.

%prep
%setup -q

%build
%{__libtoolize}
%{__aclocal}
%{__autoheader}
%{__autoconf}
%{__automake}
%configure \
	--with-mm-opts="INSTALLDIRS=vendor" \
	--enable-perl-glue \
	--with-apache2-apxs=%{apxs} \
	%{!?with_static_libs:--disable-static}

%{__make}

%{?with_tests:%{__make} test}

%install
rm -rf $RPM_BUILD_ROOT

%{__make} install \
	DESTDIR=$RPM_BUILD_ROOT

rm -f $RPM_BUILD_ROOT%{perl_vendorarch}/APR/{Request.pod,Request/*.pod}
rm -f $RPM_BUILD_ROOT%{_pkglibdir}/mod_apreq2.{a,la}
install -D %{SOURCE1} $RPM_BUILD_ROOT%{_sysconfdir}/httpd.conf/76_mod_apreq2.conf

%clean
rm -rf $RPM_BUILD_ROOT

%post	-p /sbin/ldconfig
%postun	-p /sbin/ldconfig

%post -n apache-mod_apreq2
%service -q httpd restart

%preun -n apache-mod_apreq2
if [ "$1" = "0" ]; then
	%service -q httpd restart
fi

%files
%defattr(644,root,root,755)
%doc CHANGES README
%attr(755,root,root) %{_libdir}/libapreq2.so.*.*

%files devel
%defattr(644,root,root,755)
%attr(755,root,root) %{_libdir}/libapreq2.so
%{_libdir}/libapreq2.la
%{_includedir}/apreq2
%attr(755,root,root) %{_bindir}/apreq2-config
%dir %{_includedir}/apache/apreq2
%{_includedir}/apache/apreq2/apreq_module_apache2.h

%if %{with static_libs}
%files static
%defattr(644,root,root,755)
%{_libdir}/libapreq2.a
%endif

%files -n perl-%{name}
%defattr(644,root,root,755)
%{perl_vendorarch}/Apache2/*.pm
%{perl_vendorarch}/APR/*.pm
%dir %{perl_vendorarch}/APR/Request
%{perl_vendorarch}/APR/Request/*.pm
%dir %{perl_vendorarch}/auto/APR/Request
%dir %{perl_vendorarch}/auto/APR/Request/*
%{perl_vendorarch}/auto/APR/Request/*/*.bs
%attr(755,root,root) %{perl_vendorarch}/auto/APR/Request/*/*.so

# TODO: generate these manually; Makefile.PL (and overall logic) is broken
%{_mandir}/man3/Apache*
%{_mandir}/man3/APR*

%files -n apache-mod_apreq2
%defattr(644,root,root,755)
%attr(640,root,root) %config(noreplace) %verify(not md5 mtime size) %{_sysconfdir}/httpd.conf/*_mod_apreq2.conf
%attr(755,root,root) %{_pkglibdir}/mod_apreq2.so
