#
# todo:
# - split plugins into subpackages
# - disable building of libraries which exist in system (libdv,libmpeg2 etc.)
#
# Conditional build:
%bcond_without gtk	   	# disable gtk dependent stuff
%bcond_without avifile 		# disable avifile module
%bcond_without sdl	   	# disable SDL support
%bcond_without im	   	# disable imagemagick module
%bcond_without libmpeg3		# disable libmpeg3 support
%bcond_without quicktime	# disable quicktime support
#
Summary:	Video stream converter
Summary(pl):	Konwerter strumieni video
Name:		transcode
Version:	0.6.12
Release:	1
License:	GPL
Group:		Applications
Source0:	http://www.zebra.fh-weingarten.de/~transcode/pre/%{name}-%{version}.tar.gz
# Source0-md5:	550214ed9f85224423ca8c7308ed96ce
Patch0:		%{name}-altivec.patch
Patch1:		%{name}-pic.patch
Patch2:		%{name}-amfix.patch
URL:		http://www.theorie.physik.uni-goettingen.de/~ostreich/transcode/
%{?with_im:BuildRequires:	ImageMagick-devel >= 5.4.3}
%{?with_sdl:BuildRequires:	SDL-devel}
BuildRequires:	XFree86-devel
BuildRequires:	a52dec-libs-devel
BuildRequires:	autoconf
BuildRequires:	automake >= 1.3
%{?with_avifile:BuildRequires:	avifile-devel >= 3:0.7.32-0.20030219}
%{?with_gtk:BuildRequires:	gtk+-devel}
BuildRequires:	lame-libs-devel
BuildRequires:	libdv-devel
BuildRequires:	libdvdread-devel
BuildRequires:	libfame-devel
%{?with_libmpeg3:BuildRequires:	libmpeg3-devel}
BuildRequires:	libogg-devel
BuildRequires:	libtool >= 2:1.5
BuildRequires:	libvorbis-devel
BuildRequires:	libxml2-devel
%{?with_quicktime:BuildRequires:	quicktime4linux-devel >= 1.5.5}
BuildRequires:	xvid-devel
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%define		specflags	-fomit-frame-pointer

%description
Linux Video Stream Processing Tool.

%description -l pl
Linuksowe narzêdzie do obróbki strumieni video.

%package	avilib
Summary:	library to handle avi files from transcode
Summary(pl):	biblioteka do obróbki plików avi pochodz±ca z transcode
Group:		Development/Libraries

%description avilib
Avilib is part of transcode made accessible for other programs that
require it. So far I know of one such program -- ogmtools.

%description avilib -l pl
Avifile jest czê¶ci± programu transcode udostêpnion± dla innych
programów, które jej wymagaj±. Jak na razie znam jeden taki program --
ogmtools.

%prep
%setup -q
%patch0 -p1
%patch1 -p1
%patch2 -p1

%build
%{__libtoolize}
%{__aclocal}
%{__autoconf}
%{__autoheader}
%{__automake}
# ac_cv_* to avoid detection of libdivxdecore as divx4linux (leading to errors)
# or divx4linux itself (make bcond_with if you want it)
%configure \
	ac_cv_header_decore_h=no \
	ac_cv_header_encore2_h=no \
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

%{__make} install \
	DESTDIR=$RPM_BUILD_ROOT

install -D avilib/avilib.h $RPM_BUILD_ROOT%{_includedir}/avilib.h
install avilib/libavi.a $RPM_BUILD_ROOT%{_libdir}

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr(644,root,root,755)
%doc README ChangeLog docs/README* docs/*.txt docs/html
%attr(755,root,root) %{_bindir}/*
# todo: split it into subpackages export-*, import-* and filter-*
%dir %{_libdir}/%{name}
%attr(755,root,root) %{_libdir}/%{name}/*.so*
%attr(755,root,root) %{_libdir}/%{name}/*.awk
%{_libdir}/%{name}/*.la
%{_libdir}/%{name}/*.conf
%{_libdir}/%{name}/*.cfg
%{_mandir}/man1/*

%files avilib
%defattr(644,root,root,755)
%doc avilib/README.avilib
%{_includedir}/avilib.h
%{_libdir}/libavi.a
