#
# todo:
# - split plugins into subpackages
# - disable building libraries what exists in system (libdv,libmpeg2 etc.)
#

Summary:	Video stream converter
Summary(pl):	Konwerter strumieni video
Name:		transcode
Version:	0.6.3
Release:	1
License:	GPL
Group:		Applications
Source0:	http://www.theorie.physik.uni-goettingen.de/~ostreich/transcode/pre/%{name}-%{version}.tar.gz
Patch0:		%{name}-altivec.patch
URL:		http://www.theorie.physik.uni-goettingen.de/~ostreich/transcode/
BuildRequires:	ImageMagick-devel >= 5.4.3
BuildRequires:	a52dec-libs-devel
BuildRequires:	avifile-devel >= 0.7.32-0.20030219
BuildRequires:	lame-libs-devel
BuildRequires:	libdv-devel
BuildRequires:	libdvdread-devel
BuildRequires:	libfame-devel
BuildRequires:	libmpeg3-devel
BuildRequires:	libxml2-devel
BuildRequires:	libvorbis-devel
BuildRequires:	libogg-devel
BuildRequires:	openquicktime-devel
BuildRequires:	quicktime4linux-devel >= 1.5.5
BuildRequires:	xvid-devel
BuildRequires:	XFree86-devel
BuildRequires:	SDL-devel
BuildRequires:	gtk+-devel
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%description
Linux Video Stream Processing Tool.

%description -l pl
Linuksowe narzêdzie do obróbki strumieni video.

%package	avilib
Summary:	library to handle avi files from transcode
Summary(pl):	biblioteka do obróbki plików avi pochodz±ca z transcode
Group:		Development/Libraries

%description	avilib
Avilib is part of transcode made accessible for other programs that require
it. So far I know of one such program -- ogmtools.

%description	avilib -l pl
Avifile jest czê¶ci± programu transcode udostêpnion± dla innych programów,
które jej wymagaj±. Jak na razie znam jeden taki program -- ogmtools.

%prep
%setup  -q
%patch0 -p1

%build
rm -f missing
%{__gettextize}
%{__libtoolize}
%{__aclocal}
%{__autoheader}
%{__autoconf}
#%%{__automake}
%configure \
	--with-avifile-mods \
	--with-avifile-exec-prefix=%{_prefix} \
	--with-lame \
	--with-lame-includes=%{_prefix} \
	--with-lame-libs=%{_prefix} \
	--with-ogg \
	--with-ogg-includes=%{_prefix} \
	--with-ogg-libs=%{_prefix} \
	--with-vorbis \
	--with-vorbis-includes=%{_prefix} \
	--with-vorbis-libs=%{_prefix} \
	--with-dvdread \
	--with-dvdread-includes=%{_prefix} \
	--with-dvdread-libs=%{_prefix} \
	--with-libmpeg3 \
	--with-libmpeg3-includes=%{_prefix} \
	--with-libmpeg3-libs=%{_prefix} \
	--with-qt \
	--with-qt-includes=%{_prefix} \
	--with-qt-libs=%{_prefix} \
	--with-openqt \
	--with-openqt-includes=%{_prefix} \
	--with-openqt-libs=%{_prefix} \
	--with-dv \
	--with-dv-includes=%{_prefix} \
	--with-dv-libs=%{_prefix} \
	--with-a52 \
	--with-a52-include=%{_prefix} \
	--with-a52-libs=%{_prefix} \
	--with-x \
	--with-sdl-prefix=%{_prefix} \
	--with-sdl-exec-prefix=%{_prefix} \
	--with-gtk-prefix=%{_prefix} \
	--with-gtk-exec-prefix=%{_prefix} \
	--with-libfame-prefix=%{_prefix} \
	--with-libfame-exec-prefix=%{_prefix} \
	--with-magick-mods \
	--with-magick-exec-prefix=%{_prefix} \
%ifarch ppc
	--without-altivec \
%endif
	--with-libjpeg-mods

%{__make}

%install
rm -rf $RPM_BUILD_ROOT

%{__make} install DESTDIR=$RPM_BUILD_ROOT

install -D avilib/avilib.h $RPM_BUILD_ROOT/%{_includedir}/avilib.h
install avilib/libavi.a $RPM_BUILD_ROOT/%{_libdir}

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr(644,root,root,755)
%doc README ChangeLog docs/README* docs/*.txt docs/html
%attr(755,root,root) %{_bindir}/*
# todo: split it into subpackages export-*, import-* and filter-*
%attr(755,root,root) %{_libdir}/%{name}/*.so*
%{_libdir}/%{name}/*.la
%{_mandir}/man1/*
%{_libdir}/%{name}/*.conf
%{_libdir}/%{name}/*.cfg

%files avilib
%defattr(644,root,root,755)
%doc avilib/README.avilib
%attr(644,root,root) %{_includedir}/avilib.h
%attr(644,root,root) %{_libdir}/libavi.a
