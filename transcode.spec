Summary:	Video stream converter
Summary(pl):	Konwerter strumieni video
Name:		transcode
Version:	0.6.0pre2
Release:	1
License:	GPL
Group:		Applications
#Source0:	http://www.theorie.physik.uni-goettingen.de/~ostreich/transcode/%{name}-%{version}.tgz
Source0:	http://www.theorie.physik.uni-goettingen.de/~ostreich/transcode/pre/%{name}-%{version}.tgz
Patch0:		%{name}-magick-config.patch
Patch1:		%{name}-as.patch
URL:		http://www.theorie.physik.uni-goettingen.de/~ostreich/transcode/
BuildRequires:	ImageMagick-devel >= 5.4.0
BuildRequires:	a52dec-libs-devel
BuildRequires:	avifile-devel >= 0.6.0-0.20011220admin.1
BuildRequires:	lame-libs-devel
BuildRequires:	libdv-devel
BuildRequires:	libdvdread-devel
BuildRequires:	libmpeg3-devel
BuildRequires:	openquicktime-devel
BuildConflicts:	quicktime4linux-devel
BuildConflicts:	ac3dec-devel
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%description
Linux Video Stream Processing Tool.

%description -l pl
Linuksowe narzêdzie do obróbki strumieni video.

%prep
%setup  -q
%patch0 -p1
%patch1 -p1

%build
aclocal
autoconf
automake -a -c
%configure \
--with-dv-includes=%{_prefix}/X11R6 \
--with-dv-libs=%{_prefix}/X11R6 \
--with-magick-exec-prefix=%{_prefix}/X11R6

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
%attr(755,root,root) %{_bindir}/*
# todo: split it into subpackages export-*, import-* and filter-*
%attr(755,root,root) %{_libdir}/%{name}/*.so
%attr(755,root,root) %{_libdir}/%{name}/*.la
%{_libdir}/%{name}/*.conf
