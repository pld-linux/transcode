# TODO:
# - split plugins into subpackages. (how? splitting criteria? perhaps by external deps, not by functionality (import/export/..?)
# - disable building of libraries which exist in system (libdv?,libmpeg2 etc.)
# - cmov test is broken, ignores --enable-cmov-extension and tries to read /proc/cpuinfo
# - pvm3 needs recompiled with -fPIC, then it can be used here
#
# Conditional build:
%bcond_without	avifile 	# disable avifile module
%bcond_without	gtk			# disable GTK+ dependent stuff
%bcond_without	im			# disable imagemagick module
%bcond_without	libmpeg2	# disable libmpeg2 support
%bcond_without	libmpeg3	# disable libmpeg3 support
%bcond_without	lzo			# disable lzo support
%bcond_without	mjpeg		# disable mjpegtools support
%bcond_without	sdl			# disable SDL support
%bcond_with	jpegmmx		# jpeg-mmx
%bcond_with	pvm3		# pvm3

# no jpeg-mmx there (doesn't compile)
%ifnarch i586 i686 athlon
%undefine	with_jpegmmx
%endif
# pvm3 needs recompiled with -fPIC
%ifarch %{x8664} alpha
%undefine	with_pvm3
%endif
#
Summary:	Video stream converter
Summary(pl):	Konwerter strumieni video
Name:		transcode
Version:	1.0.2
Release:	3
License:	GPL
Group:		Applications
Source0:	http://www.jakemsr.com/transcode/%{name}-%{version}.tar.gz
# Source0-md5:	e353c0ab7e927a8672528e05a9ae960b
Patch0:		%{name}-ac.patch
Patch1:		%{name}-lzo2.patch
Patch2:		%{name}-bigdir.patch
Patch3:		%{name}-mpeg3.patch
Patch4:		%{name}-libx86_64.patch
Patch5:		%{name}-ffmpeg.patch
URL:		http://www.transcoding.org/
%{?with_im:BuildRequires:	ImageMagick-devel >= 5.4.3}
%{?with_sdl:BuildRequires:	SDL-devel >= 1.1.6}
BuildRequires:	XFree86-devel
BuildRequires:	a52dec-libs-devel
BuildRequires:	autoconf
BuildRequires:	automake >= 1.3
%{?with_avifile:BuildRequires:	avifile-devel > 3:0.7.43-1}
BuildRequires:	ffmpeg-devel >= 0.4.9-0.pre1
BuildRequires:	freetype-devel >= 2.1.2
%{?with_gtk:BuildRequires:	gtk+-devel}
%{?with_jpegmmx:BuildRequires:	jpeg-mmx}
BuildRequires:	lame-libs-devel >= 3.89
BuildRequires:	libdv-devel >= 0.104-3
BuildRequires:	libdvdread-devel
BuildRequires:	libfame-devel
BuildRequires:	libjpeg-devel
%{?with_libmpeg3:BuildRequires:	libmpeg3-devel}
BuildRequires:	libogg-devel
BuildRequires:	libpng-devel
%{?with_quicktime:BuildRequires:	libquicktime-devel}
BuildRequires:	libstdc++-devel
BuildRequires:	libtheora-devel
BuildRequires:	libtool >= 2:1.5
BuildRequires:	libvorbis-devel
BuildRequires:	libxml2-devel
%{?with_lzo:BuildRequires:	lzo-devel >= 2.0}
%{?with_mjpeg:BuildRequires:	mjpegtools-devel}
%{?with_libmpeg2:BuildRequires:	mpeg2dec-devel >= 0.4.0b}
%ifarch %{ix86}
BuildRequires:	nasm >= 0.98.34
%endif
BuildRequires:	pkgconfig
%{?with_pvm3:BuildRequires:	pvm-devel}
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
%patch0 -p1
%patch1 -p1
%patch2 -p0
%patch3 -p0
%patch4 -p0
%patch5 -p1

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
%ifarch ppc
	--disable-altivec \
%endif
%ifarch %{ix86} %{x8664}
	--enable-mmx \
	--enable-3dnow \
	--enable-sse \
	--enable-sse2 \
%endif
%ifarch %{ix86}
%ifarch i386 i486 i586 \
	--disable-cmov-extension \
%else
	--enable-cmov-extension \
%endif
%endif
	--disable-bktr \
	--disable-bsdav \
	--disable-sunau \
	--enable-a52 \
	--enable-a52-default-decoder \
	--enable-freetype2 \
	--%{!?with_gtk:dis}%{?with_gtk:en}able-gtk \
	--enable-ibp \
	--enable-iconv \
	--enable-imagemagick \
	--enable-lame \
	--enable-libavcodec \
	--enable-libdv \
	--enable-libdvdread \
	--enable-libfame \
	--enable-libjpeg \
	--%{!?with_libmpeg2:dis}%{?with_libmpeg2:en}able-libmpeg2 \
	--%{!?with_libmpeg3:dis}%{?with_libmpeg3:en}able-libmpeg3 \
	--enable-libpostproc \
	--%{!?with_quicktime:dis}%{?with_quicktime:en}able-libquicktime \
	--enable-libxml2 \
	--%{!?with_lzo:dis}%{?with_lzo:en}able-lzo \
	--with-lzo-includes=%{_includedir}/lzo \
	--%{!?with_mjpeg:dis}%{?with_mjpeg:en}able-mjpegtools \
	--enable-netstream \
	--enable-ogg \
	--enable-oss \
	--enable-sdl \
	--enable-statbuffer \
	--enable-theora \
	--enable-v4l \
	--enable-vorbis \
	--enable-xio \
	--%{!?with_avifile:dis}%{?with_avifile:en}able-avifile \
	--%{!?with_jpegmmx:dis}%{?with_jpegmmx:en}able-libjpegmmx \
	--%{!?with_pvm3:dis}%{?with_pvm3:en}able-pvm3 \
	--with-libpostproc-includes=%{_includedir}/postproc \
	--with-x

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
