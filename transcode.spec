Summary:	Video stream converter
Summary(pl):	Konwerter strumieni video
Name:		transcode
Version:	0.5.3
Release:	1
License:	GPL
Group:		Applications
Group(de):	Applikationen
Group(es):	Aplicaciones
Group(pl):	Aplikacje
Group(pt):	Aplicações
Group(pt_BR):	Aplicações
Source0:	http://www.theorie.physik.uni-goettingen.de/~ostreich/transcode/%{name}-%{version}.tgz
URL:		http://www.theorie.physik.uni-goettingen.de/~ostreich/transcode/
BuildRequires:	a52dec-libs-devel
BuildRequires:	avifile-devel
BuildRequires:	lame-libs-devel
BuildRequires:	libdv-devel
BuildRequires:	libdvdread-devel
BuildRequires:	libmpeg3-devel
BuildRequires:	quicktime4linux-devel
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%description
Linux Video Stream Processing Tool.

%description -l pl
Linuksowe narzêdzie do obróbki strumieni video.

%prep
%setup  -q

%build
%configure \
	--with-dv-includes=/usr/X11R6 \
	--with-dv-libs=/usr/X11R6

%{__make}

%install
rm -rf $RPM_BUILD_ROOT

%{__make} install DESTDIR=$RPM_BUILD_ROOT

gzip -9nf README ChangeLog

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr(644,root,root,755)
%doc *.gz
