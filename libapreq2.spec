Summary:	Apache Request Library
Summary(pl):	Biblioteka ¿±dañ Apache
Name:		libapreq2
%define		_devel	02
Version:	2.02
Release:	0.%{_devel}.1
License:	Apache Group
Group:		Libraries
Source0:	http://www.apache.org/dist/httpd/libapreq/%{name}-%{version}_%{_devel}-dev.tar.gz
# Source0-md5:	dbca30cd45ec88c642ef38ae6d229865
URL:		http://httpd.apache.org/apreq/
BuildRequires:	apache-devel >= 2.0.46
BuildRequires:	apache-mod_perl >= 2.0
BuildRequires:	perl-ExtUtils-XSBuilder >= 0.23
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
Requires:	%{name} = %{version}

%description devel
libapreq2 header files.

%description devel -l pl
Pliki nag³ówkowe biblioteki libapreq2.

# %package static
# Summary:	libapreq static library
# Summary(pl):	Statyczna biblioteka libapreq
# Group:		Development/Libraries
# Requires:	%{name}-devel = %{version}
# 
# %description static
# Static version of libapreq library.
# 
# %description static -l pl
# Statyczna wersja biblioteki libapreq.

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
%configure \
	--enable-perl-glue

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

# %files static
# %defattr(644,root,root,755)
# %{_libdir}/*.a

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
