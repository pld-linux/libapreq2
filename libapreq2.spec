%include	/usr/lib/rpm/macros.perl
%define	apxs	/usr/sbin/apxs
Summary:	Apache Request Library
Summary(pl):	Biblioteka ¿±dañ Apache
Name:		libapreq2
%define	_devel	04
Version:	2.03
Release:	0.%{_devel}.5
License:	Apache Group
Group:		Libraries
Source0:	http://www.apache.org/dist/httpd/libapreq/%{name}-%{version}_%{_devel}-dev.tar.gz
# Source0-md5:	18cefa860f15812ed35c5e1eb52f9a0a
URL:		http://httpd.apache.org/apreq/
BuildRequires:	apache-devel >= 2.0.46
BuildRequires:	apache-mod_perl >= 1.99
BuildRequires:	%{apxs}
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
%{__libtoolize}
%{__aclocal}
%{__autoheader}
%{__autoconf}
%{__automake}
%configure \
	--enable-perl-glue \
	--with-apache2-apxs=%{apxs}

%{__make} -C src

cd glue/perl
%{__perl} Makefile.PL \
	INSTALLDIRS=vendor
%{__make} \
	OPTIMIZE="%{rpmcflags}"
cd ../..
# TODO: mod_apreq

%install
rm -rf $RPM_BUILD_ROOT

%{__make} -C src install \
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

%files static
%defattr(644,root,root,755)
%{_libdir}/*.a

%files -n perl-%{name}
%defattr(644,root,root,755)
%{perl_vendorarch}/Apache/*.pm
%dir %{perl_vendorarch}/auto/Apache/Cookie
%dir %{perl_vendorarch}/auto/Apache/Request
%{perl_vendorarch}/auto/Apache/Cookie/Cookie.bs
%{perl_vendorarch}/auto/Apache/Request/Request.bs
%attr(755,root,root) %{perl_vendorarch}/auto/Apache/Cookie/Cookie.so
%attr(755,root,root) %{perl_vendorarch}/auto/Apache/Request/Request.so
%{_mandir}/man3/Apache*
