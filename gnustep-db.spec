Summary:	The GNUstep Database Library
Summary(pl):	Biblioteka baz danych GNUstepa
Name:		gnustep-db
Version:	1.2.0
Release:	1
License:	LGPL
Group:		Libraries
Source0:	ftp://ftp.gnustep.org/pub/gnustep/db/gstep-db-%{version}.tar.gz
Patch0:		%{name}-update.patch
Patch1:		%{name}-rootdir.patch
Patch2:		%{name}-paths.patch
Patch3:		%{name}-link.patch
URL:		http://www.gnustep.org/
BuildRequires:	freetds-devel
BuildRequires:	gnustep-base-devel
BuildRequires:	gnustep-extensions-devel
BuildRequires:	postgresql-backend-devel
BuildRequires:	postgresql-devel
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%define		_gsdir		/usr/lib/GNUstep

%define		libcombo	gnu-gnu-gnu
%define		gsos		linux-gnu
%ifarch %{ix86}
%define		gscpu		ix86
%else
# also s/alpha.*/alpha/, but we use only "alpha" arch for now
%define		gscpu		%{_target_cpu}
%endif

%description
The GNUstep Database Library is a hierarchy of Objective-C classes
that provide a three-tiered architecture for developing database
applications.
   
%description -l pl
GNUstep Database Library, czyli biblioteka baz danych GNUstepa, to
hierarchia klas Objective-C, udost�pniaj�ca tr�jwarstwow� architektur�
do tworzenia aplikacji bazodanowych.

%package devel
Summary:	Header files for GNUstep Database Library
Summary(pl):	Pliki nag��wkowe biblioteki baz danych GNUstepa
Group:		Development/Libraries
Requires:	%{name} = %{version}

%description devel
Header files for GNUstep Database Library.

%description devel -l pl
Pliki nag��wkowe biblioteki baz danych GNUstepa.

%package postgresql
Summary:	PostgreSQL adaptor for GNUstep Database Library
Summary(pl):	Interfejs PostgreSQL dla biblioteki baz danych GNUstepa
Group:		Libraries
Requires:	%{name} = %{version}

%description postgresql
PostgreSQL adaptor for GNUstep Database Library.

%description postgresql -l pl
Interfejs PostgreSQL dla biblioteki baz danych GNUstepa.

%package postgresql-devel
Summary:	Header files for GNUstep PostgreSQL adaptor
Summary(pl):	Pliki nag��wkowe interfejsu PostgreSQL do GNUstepa
Group:		Development/Libraries
Requires:	%{name}-devel = %{version}
Requires:	%{name}-postgresql = %{version}

%description postgresql-devel
Header files for GNUstep PostgreSQL adaptor.

%description postgresql-devel -l pl
Pliki nag��wkowe interfejsu PostgreSQL do GNUstepa.

%package sybase
Summary:	Sybase/MS SQL adaptor for GNUstep Database Library
Summary(pl):	Interfejs Sybase/MS SQL dla biblioteki baz danych GNUstepa
Group:		Libraries
Requires:	%{name} = %{version}

%description sybase
Sybase/MS SQL adaptor for GNUstep Database Library.

%description sybase -l pl
Interfejs Sybase/MS SQL dla biblioteki baz danych GNUstepa.

%package sybase-devel
Summary:	Header files for GNUstep Sybase/MS SQL adaptor
Summary(pl):	Pliki nag��wkowe interfejsu Sybase/MS SQL do GNUstepa
Group:		Development/Libraries
Requires:	%{name}-devel = %{version}
Requires:	%{name}-sybase = %{version}

%description sybase-devel
Header files for GNUstep Sybase/MS SQL adaptor.

%description sybase-devel -l pl
Pliki nag��wkowe interfejsu Sybase/MS SQL do GNUstepa.

%prep
%setup -q -n gstep-db-%{version}
%patch0 -p1
%patch1 -p1
%patch2 -p1
%patch3 -p1

%build
. %{_gsdir}/System/Makefiles/GNUstep.sh
SYBASE_CLAGS=" " SYBASE_LDFLAGS="-lsybdb"
POSTGRES95_CFLAGS="-I/usr/include/postgresql/server" POSTGRES95_LDFLAGS="-lpq"
export SYBASE_CFLAGS SYBASE_LDFLAGS POSTGRES95_CFLAGS POSTGRES95_LDFLAGS
%configure2_13 \
	--with-postgres95 \
	--with-sybase

%{__make} \
	messages=yes

cd doc
for f in gdl version news ; do
	ln -sf $f.tmpl.texi $f.texi
done
%{__make}

%install
rm -rf $RPM_BUILD_ROOT
. %{_gsdir}/System/Makefiles/GNUstep.sh
%{__make} install \
	INSTALL_ROOT_DIR=$RPM_BUILD_ROOT \
	GNUSTEP_INSTALLATION_DIR=$RPM_BUILD_ROOT%{_gsdir}/System \
	GNUSTEP_LIBRARIES_ROOT=$RPM_BUILD_ROOT%{_gsdir}/System/Library/Bundles

mv -f eoadaptors/README README.eoadaptors

%{__make} -C doc install \
	GNUSTEP_INSTALLATION_DIR=$RPM_BUILD_ROOT%{_gsdir}/System
# not (yet?) supported by rpm-compress-doc
find $RPM_BUILD_ROOT%{_gsdir}/System/Documentation \
	-type f -a ! -name '*.html' | xargs gzip -9nf

%clean
rm -rf $RPM_BUILD_ROOT

%post	-p /sbin/ldconfig
%postun	-p /sbin/ldconfig

%post	postgresql -p /sbin/ldconfig
%postun	postgresql -p /sbin/ldconfig

%post	sybase -p /sbin/ldconfig
%postun	sybase -p /sbin/ldconfig

%files
%defattr(644,root,root,755)
%doc AUTHORS ChangeLog SUPPORT TODO README.eoadaptors eointerface/EOController.README
# ANNOUNCE INSTALL NEWS README
%docdir %{_prefix}/System/Documentation
%{_gsdir}/System/Documentation/Developer/GDL
%{_gsdir}/System/Documentation/info/*.info*

%dir %{_gsdir}/System/Library/Bundles/Adaptors

%attr(755,root,root) %{_gsdir}/System/Libraries/%{gscpu}/%{gsos}/%{libcombo}/libgnustep-db*.so.*

%files devel
%defattr(644,root,root,755)

%{_gsdir}/System/Headers/gnustep/eoaccess
%dir %{_gsdir}/System/Headers/gnustep/eoadaptors
%{_gsdir}/System/Headers/gnustep/eointerface

%attr(755,root,root) %{_gsdir}/System/Libraries/%{gscpu}/%{gsos}/%{libcombo}/libgnustep-db*.so

%{_gsdir}/System/Makefiles/gdl.make

%files postgresql
%defattr(644,root,root,755)
%doc eoadaptors/Postgres95/README
%dir %{_gsdir}/System/Library/Bundles/Adaptors/Postgres95.gdladaptor
%{_gsdir}/System/Library/Bundles/Adaptors/Postgres95.gdladaptor/Resources
%attr(755,root,root) %{_gsdir}/System/Library/Bundles/Adaptors/Postgres95.gdladaptor/%{gscpu}
%attr(755,root,root) %{_gsdir}/System/Libraries/%{gscpu}/%{gsos}/%{libcombo}/libgdl-postgresql.so.*

%files postgresql-devel
%defattr(644,root,root,755)
%{_gsdir}/System/Headers/gnustep/eoadaptors/PostgreSQL
%attr(755,root,root) %{_gsdir}/System/Libraries/%{gscpu}/%{gsos}/%{libcombo}/libgdl-postgresql.so

%files sybase
%defattr(644,root,root,755)
%doc eoadaptors/Sybase/README
%attr(755,root,root) %{_gsdir}/System/Libraries/%{gscpu}/%{gsos}/%{libcombo}/libgnustep-db*.so.*
%attr(755,root,root) %{_gsdir}/System/Libraries/%{gscpu}/%{gsos}/%{libcombo}/libgdl-sybase.so.*

%files sybase-devel
%defattr(644,root,root,755)
%{_gsdir}/System/Headers/gnustep/eoadaptors/Sybase
%attr(755,root,root) %{_gsdir}/System/Libraries/%{gscpu}/%{gsos}/%{libcombo}/libgdl-sybase.so