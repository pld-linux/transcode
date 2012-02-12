# TODO:
# - disable building of libraries which exist in system (libdv?,libmpeg2 etc.)
# - cmov test is broken, ignores --enable-cmov-extension and tries to read /proc/cpuinfo
# - pvm3 needs recompiled with -fPIC, then it can be used here
# - --enable-xio requires some libs from http://loci.cs.utk.edu/
# - rm Makefiles from htmldir
#
# Conditional build:
%bcond_without	im			# disable imagemagick module
%bcond_without	libmpeg2	# disable libmpeg2 support
%bcond_without	lzo			# disable lzo support
%bcond_without	mjpeg		# disable mjpegtools support
%bcond_without	quicktime	# disable libquicktime support
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
Summary(pl.UTF-8):	Konwerter strumieni video
Name:		transcode
Version:	1.1.5
Release:	4
License:	GPL
Group:		Applications
Source0:	http://download.berlios.de/tcforge/%{name}-%{version}.tar.bz2
# Source0-md5:	41ac6b1c0fe30f3aab286e771fc31b9e
Patch0:		%{name}-libx86_64.patch
Patch1:		%{name}-ImageMagick.patch
Patch2:		%{name}-mpa.patch
Patch3:		%{name}-ffmpeg.patch
URL:		http://tcforge.berlios.de/
%{?with_im:BuildRequires:	ImageMagick-devel >= 6.4.1-2}
%{?with_sdl:BuildRequires:	SDL-devel >= 1.1.6}
BuildRequires:	a52dec-libs-devel
BuildRequires:	autoconf
BuildRequires:	automake >= 1.3
BuildRequires:	ffmpeg-devel >= 0.7.1
BuildRequires:	freetype-devel >= 2.1.2
%{?with_jpegmmx:BuildRequires:	jpeg-mmx}
BuildRequires:	lame-libs-devel >= 3.89
BuildRequires:	libdv-devel >= 0.104-3
BuildRequires:	libdvdread-devel
BuildRequires:	libfame-devel >= 0.9.1
BuildRequires:	libgomp-devel
BuildRequires:	libjpeg-devel
%{?with_libmpeg2:BuildRequires:	libmpeg2-devel >= 0.4.0b}
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
%ifarch %{ix86}
BuildRequires:	nasm >= 0.98.34
%endif
BuildRequires:	pkgconfig
%{?with_pvm3:BuildRequires:	pvm-devel}
BuildRequires:	xorg-lib-libXaw-devel
BuildRequires:	xorg-lib-libXpm-devel
BuildRequires:	xvid-devel
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%define		specflags	-fomit-frame-pointer

%description
Linux Video Stream Processing Tool.

%description -l pl.UTF-8
Linuksowe narzędzie do obróbki strumieni video.

%package avilib
Summary:	library to handle avi files from transcode
Summary(pl.UTF-8):	biblioteka do obróbki plików avi pochodząca z transcode
Group:		Development/Libraries

%description avilib
Avilib is part of transcode made accessible for other programs that
require it. So far I know of one such program - ogmtools.

%description avilib -l pl.UTF-8
Avifile jest częścią programu transcode udostępnioną dla innych
programów, które jej wymagają. Jak na razie znam jeden taki program -
ogmtools.

%package export
Summary:	export plugins for transcode
Summary(pl.UTF-8):	wtyczki eksportowe transcode
Group:		Development/Libraries
Requires:	%{name} = %{version}-%{release}

%description export
Export plugins for transcode.

%description export -l pl.UTF-8
Wtyczki eksportowe dla transcode.

%package import
Summary:	import plugins for transcode
Summary(pl.UTF-8):	wtyczki importujące transcode
Group:		Development/Libraries
Requires:	%{name} = %{version}-%{release}

%description import
Import plugins for transcode.

%description import -l pl.UTF-8
Wtyczki importujące dla transcode.

%package filter
Summary:	filters for transcode
Summary(pl.UTF-8):	filtry transcode
Group:		Development/Libraries
Requires:	%{name} = %{version}-%{release}

%description filter
Filters for transcode.

%description filter -l pl.UTF-8
Filtry transcode.

%prep
%setup -q
%patch0 -p1
%patch1 -p1
%patch2 -p1
%patch3 -p1

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
	--enable-altivec \
%endif
%ifarch %{ix86} %{x8664}
	--enable-mmx \
	--enable-3dnow \
	--enable-sse \
	--enable-sse2 \
%endif
	--disable-bktr \
	--disable-bsdav \
	--disable-sunau \
	--enable-a52 \
	--enable-freetype2 \
	--enable-iconv \
	--%{!?with_im:dis}%{?with_im:en}able-imagemagick \
	--enable-lame \
	--enable-libavcodec \
	--enable-libdv \
	--enable-libdvdread \
	--enable-libjpeg \
	--%{!?with_libmpeg2:dis}%{?with_libmpeg2:en}able-libmpeg2 \
	--enable-libpostproc \
	--%{!?with_quicktime:dis}%{?with_quicktime:en}able-libquicktime \
	--enable-libxml2 \
	--%{!?with_lzo:dis}%{?with_lzo:en}able-lzo \
	--with-lzo-includes=%{_includedir}/lzo \
	--%{!?with_mjpeg:dis}%{?with_mjpeg:en}able-mjpegtools \
	--enable-ogg \
	--enable-oss \
	--enable-sdl \
	--enable-statbuffer \
	--enable-theora \
	--enable-v4l \
	--enable-vorbis \
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
%dir %{_libdir}/%{name}
%{_libdir}/%{name}/a52_decore.la
%{_libdir}/%{name}/a52_decore.so
%{_libdir}/%{name}/parse_csv.awk
%{_libdir}/%{name}/*.cfg
%{_mandir}/man1/*

%files avilib
%defattr(644,root,root,755)
%doc avilib/README.avilib
%{_includedir}/avilib.h

%files export
%defattr(644,root,root,755)
%attr(755,root,root) %{_libdir}/%{name}/export*.la*
%attr(755,root,root) %{_libdir}/%{name}/export*.so*

%files import
%defattr(644,root,root,755)
%attr(755,root,root) %{_libdir}/%{name}/import*.la*
%attr(755,root,root) %{_libdir}/%{name}/import*.so*

%files filter
%defattr(644,root,root,755)
%attr(755,root,root) %{_libdir}/%{name}/filter*.la*
%attr(755,root,root) %{_libdir}/%{name}/filter*.so*
%attr(755,root,root) %{_libdir}/%{name}/filter*.awk
