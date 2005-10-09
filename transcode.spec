# TODO:
# - split plugins into subpackages. (how? splitting criteria? perhaps by external deps, not by functionality (import/export/..?)
# - disable building of libraries which exist in system (libdv?,libmpeg2 etc.)
# - cmov test is broken, ignores --enable-cmov-extension and tries to read /proc/cpuinfo
# - pvm3 needs recompiled with -fPIC, then it can be used here
#
# Conditional build:
%bcond_without	gtk		# disable GTK+ dependent stuff
%bcond_without	avifile 		# disable avifile module
%bcond_without	sdl		# disable SDL support
%bcond_without	im		# disable imagemagick module
%bcond_without	libmpeg3		# disable libmpeg3 support
%bcond_without	quicktime	# build with quicktime4linux support
%bcond_with	jpegmmx	# jpeg-mmx
%bcond_without	pvm3	# pvm3

# no jpeg-mmx there (doesn't compile)
%ifnarch i586 i686 athlon
%undefine	with_jpegmmx
%endif
# pvm3 needs recompiled with -fPIC
%ifarch amd64
%undefine	with_pvm3
%endif
#
Summary:	Video stream converter
Summary(pl):	Konwerter strumieni video
Name:		transcode
Version:	1.0.1
Release:	0.3
License:	GPL
Group:		Applications
Source0:	http://www.jakemsr.com/transcode/%{name}-%{version}.tar.gz
# Source0-md5:	6fd4bc7651ebccdcd384474eb557d160
Patch0:		%{name}-altivec.patch
Patch1:		%{name}-pic.patch
Patch2:		%{name}-amfix.patch
Patch3:		%{name}-gcc34.patch
Patch4:		%{name}-libdv-0.103.patch
URL:		http://www.transcoding.org/
%{?with_im:BuildRequires:	ImageMagick-devel >= 5.4.3}
%{?with_sdl:BuildRequires:	SDL-devel >= 1.1.6}
BuildRequires:	XFree86-devel
BuildRequires:	a52dec-libs-devel
# was required, maybe it was indirect. don't know ;(
BuildRequires:	artsc-devel
BuildRequires:	autoconf
BuildRequires:	automake >= 1.3
%{?with_avifile:BuildRequires:	avifile-devel >= 3:0.7.32-0.20030219}
BuildRequires:	freetype-devel >= 2.1.2
BuildRequires:	glib-devel >= 0.99.7
%{?with_gtk:BuildRequires:	gtk+-devel}
%{?with_jpegmmx:BuildRequires:	jpeg-mmx}
BuildRequires:	lame-libs-devel >= 3.89
BuildRequires:	libdv-devel >= 0.103
BuildRequires:	libdvdread-devel
BuildRequires:	libfame-devel
BuildRequires:	libjpeg-devel
%{?with_libmpeg3:BuildRequires:	libmpeg3-devel}
# liblve-devel ???
BuildRequires:	libogg-devel
BuildRequires:	libtheora-devel
BuildRequires:	libtool >= 2:1.5
BuildRequires:	libvorbis-devel
BuildRequires:	libquicktime-devel
BuildRequires:	libxml2-devel
BuildRequires:	lzo-devel
BuildRequires:	mjpegtools-devel
BuildRequires:	mpeg2dec-devel
%ifarch %{ix86}
BuildRequires:	nasm >= 0.98.34
%endif
#%{?with_quicktime:BuildRequires:	quicktime4linux-devel >= 1.5.5}
BuildRequires:	xvid-devel
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%define		specflags	-fomit-frame-pointer

%description
Linux Video Stream Processing Tool.

%description -l pl
Linuksowe narzêdzie do obróbki strumieni video.

%package avilib
Summary:	library to handle avi files from transcode
Summary(pl):	biblioteka do obróbki plików avi pochodz±ca z transcode
Group:		Development/Libraries

%description avilib
Avilib is part of transcode made accessible for other programs that
require it. So far I know of one such program - ogmtools.

%description avilib -l pl
Avifile jest czê¶ci± programu transcode udostêpnion± dla innych
programów, które jej wymagaj±. Jak na razie znam jeden taki program -
ogmtools.

%prep
%setup -q
#%patch0 -p1
#%patch1 -p1
#%patch2 -p1
#%patch3 -p1
#%patch4 -p0

%build
%if 0
%{__libtoolize}
%{__aclocal}
%{__autoconf}
%{__autoheader}
%{__automake}
%endif
# ac_cv_* to avoid detection of libdivxdecore as divx4linux (leading to errors)
# or divx4linux itself (make bcond_with if you want it)
%configure \
	ac_cv_header_decore_h=no \
	ac_cv_header_encore2_h=no \
	--enable-mmx \
	--enable-3dnow \
	--enable-sse \
	--enable-sse2 \
%ifnarch ppc
	--enable-altivec \
%endif
%ifarch ppc
	--disable-altivec \
%endif
%ifarch %{ix86}
%ifarch i386 i486 i586 \
	--disable-cmov-extension \
%else
	--enable-cmov-extension \
%endif
%endif
	--enable-libavcodec \
	--enable-libmpeg2 \
	--enable-statbuffer \
	--enable-netstream \
	--enable-v4l \
	--disable-bktr \
	--disable-sunau \
	--enable-oss \
	--enable-ibp \
	--enable-libpostproc \
	--enable-freetype2 \
	--enable-avifile \
	--enable-lame \
	--enable-ogg \
	--enable-vorbis \
	--enable-theora \
	--enable-libdvdread \
	--%{!?with_pvm3:dis}%{?with_pvm3:en}able-pvm3 \
	--enable-libdv \
	--enable-libquicktime \
	--enable-lzo \
	--enable-a52 \
	--enable-a52-default-decoder \
	--enable-libmpeg3 \
	--enable-libxml2 \
	--enable-mjpegtools \
	--enable-sdl \
	--enable-gtk \
	--enable-libfame \
	--enable-imagemagick \
	--%{!?with_jpegmmx:dis}%{?with_jpegmmx:en}able-libjpegmmx \
	--enable-libjpeg \
	--disable-bsdav \
	--enable-iconv \
	--enable-xio \
	--with-x \
	--with-libpostproc-includes=%{_includedir}/postproc

%{__make}

%install
rm -rf $RPM_BUILD_ROOT

%{__make} install \
	DESTDIR=$RPM_BUILD_ROOT

install -D avilib/avilib.h $RPM_BUILD_ROOT%{_includedir}/avilib.h

# duplicate
rm -rf $RPM_BUILD_ROOT%{_docdir}/transcode

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr(644,root,root,755)
%doc README ChangeLog docs/README* docs/*.txt docs/html
%attr(755,root,root) %{_bindir}/*
# TODO: split it into subpackages export-*, import-* and filter-*
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
