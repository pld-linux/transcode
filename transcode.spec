# TODO:
# - pvm3 needs recompiled with -fPIC, then it can be used here
# - --enable-ibp requires some libs from http://loci.cs.utk.edu/ [libfdr libibp libexnode liblbone libend2end libmd5 libdes libaes liblors]
# - rm Makefiles from htmldir
#
# Conditional build:
%bcond_without	magick		# ImageMagick module
%bcond_without	libmpeg2	# libmpeg2 support
%bcond_without	lzo		# LZO support
%bcond_without	mjpeg		# mjpegtools support
%bcond_without	quicktime	# libquicktime support
%bcond_without	sdl		# SDL support
%bcond_with	jpegmmx		# jpeg-mmx instead of plain libjpeg
%bcond_with	pvm3		# PVM3 support

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
Version:	1.1.7
Release:	19
License:	GPL v2+
Group:		Applications/Multimedia
Source0:	https://bitbucket.org/france/transcode-tcforge/downloads/%{name}-%{version}.tar.bz2
# Source0-md5:	9bb25a796a8591fb764de46ee87ce505
Patch0:		%{name}-libx86_64.patch
Patch1:		%{name}-1.1.7-ffmpeg-0.10.patch
Patch2:		%{name}-1.1.7-ffmpeg-0.11.patch
Patch3:		%{name}-1.1.7-ffmpeg2.patch
Patch4:		%{name}-1.1.7-ffmpeg.patch
Patch5:		%{name}-1.1.7-libav-9.patch
Patch6:		%{name}-1.1.7-preset-force.patch
Patch7:		%{name}-1.1.7-preset-free.patch
Patch8:		%{name}-1.1.7-ffmpeg-2.4.patch
Patch9:		ffmpeg3.patch
Patch10:	imagemagick7.patch
Patch11:	ffmpeg4.patch
Patch12:	libav-10.patch
Patch13:	strerror.patch
Patch14:	local-static.patch
Patch15:	duplicate.patch
URL:		https://bitbucket.org/france/transcode-tcforge/overview
%{?with_magick:BuildRequires:	ImageMagick-devel >= 6.4.1-2}
%{?with_sdl:BuildRequires:	SDL-devel >= 1.2.5}
BuildRequires:	a52dec-libs-devel
BuildRequires:	alsa-lib-devel >= 0.9
BuildRequires:	autoconf
BuildRequires:	automake >= 1.3
BuildRequires:	faac-devel
BuildRequires:	ffmpeg-devel >= 0.7.1
BuildRequires:	freetype-devel >= 2.1.2
%{?with_jpegmmx:BuildRequires:	jpeg-mmx}
BuildRequires:	lame-libs-devel >= 3.93
BuildRequires:	libdv-devel >= 0.104-3
BuildRequires:	libdvdread-devel
BuildRequires:	libfame-devel >= 0.9.1
BuildRequires:	libgomp-devel
BuildRequires:	libjpeg-devel
%{?with_libmpeg2:BuildRequires:	libmpeg2-devel >= 0.4.0b}
BuildRequires:	libogg-devel
BuildRequires:	libpng-devel
%{?with_quicktime:BuildRequires:	libquicktime-devel >= 1.0.0}
BuildRequires:	libstdc++-devel
BuildRequires:	libtheora-devel
BuildRequires:	libtool >= 2:1.5
BuildRequires:	libv4l-devel
BuildRequires:	libvorbis-devel
BuildRequires:	libx264-devel
BuildRequires:	libxml2-devel >= 2.0
%{?with_lzo:BuildRequires:	lzo-devel >= 2.0}
%{?with_mjpeg:BuildRequires:	mjpegtools-devel}
%ifarch %{ix86}
BuildRequires:	nasm >= 0.98.34
%endif
BuildRequires:	pkgconfig >= 1:0.20
%{?with_pvm3:BuildRequires:	pvm-devel >= 3.4}
BuildRequires:	xorg-lib-libX11-devel
BuildRequires:	xorg-lib-libXaw-devel
BuildRequires:	xorg-lib-libXext-devel
BuildRequires:	xorg-lib-libXpm-devel
BuildRequires:	xorg-lib-libXv-devel
BuildRequires:	xvid-devel >= 1.0
BuildRequires:	zlib-devel
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
%patch1 -p0
%patch2 -p1
%patch3 -p1
%patch4 -p0
%patch5 -p0
%patch6 -p1
%patch7 -p1
%patch8 -p1
%patch9 -p1
%patch10 -p1
%patch11 -p0
%patch12 -p0
%patch13 -p1
%patch14 -p1
%patch15 -p1

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
	--enable-alsa \
	--enable-faac \
	--enable-freetype2 \
	--enable-iconv \
	--enable-imagemagick%{!?with_magick:=no} \
	--enable-lame \
	--enable-libavcodec \
	--enable-libdv \
	--enable-libdvdread \
	--enable-libjpeg \
	--enable-libjpegmmx%{!?with_jpegmmx:=no} \
	--enable-libmpeg2%{!?with_libmpeg2:=no} \
	--enable-libmpeg2convert \
	--enable-libpostproc \
	--enable-libquicktime%{!?with_quicktime:=no} \
	--enable-libv4l2 \
	--enable-libv4lconvert \
	--enable-libxml2 \
	--enable-lzo%{!?with_lzo:=no} \
	--enable-mjpegtools%{!?with_mjpeg:=no} \
	--enable-ogg \
	--enable-oss \
	--enable-pvm3%{!?with_pvm3:=no} \
	--enable-sdl \
	--enable-statbuffer \
	--enable-theora \
	--enable-v4l \
	--enable-vorbis \
	--enable-x264 \
	--with-lzo-includes=%{_includedir}/lzo \
	--with-x

%{__make}

%install
rm -rf $RPM_BUILD_ROOT

%{__make} install \
	DESTDIR=$RPM_BUILD_ROOT

install -D avilib/avilib.h $RPM_BUILD_ROOT%{_includedir}/avilib.h

# dlopened modules
%{__rm} $RPM_BUILD_ROOT%{_libdir}/%{name}/*.la
# duplicate
%{__rm} -r $RPM_BUILD_ROOT%{_docdir}/transcode

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr(644,root,root,755)
%doc AUTHORS ChangeLog README TODO docs/README.* docs/*.txt docs/html
%attr(755,root,root) %{_bindir}/avifix
%attr(755,root,root) %{_bindir}/aviindex
%attr(755,root,root) %{_bindir}/avimerge
%attr(755,root,root) %{_bindir}/avisplit
%attr(755,root,root) %{_bindir}/avisync
%attr(755,root,root) %{_bindir}/tccat
%attr(755,root,root) %{_bindir}/tcdecode
%attr(755,root,root) %{_bindir}/tcdemux
%attr(755,root,root) %{_bindir}/tcextract
%attr(755,root,root) %{_bindir}/tcmodinfo
%attr(755,root,root) %{_bindir}/tcmp3cut
%attr(755,root,root) %{_bindir}/tcprobe
%attr(755,root,root) %{_bindir}/tcscan
%attr(755,root,root) %{_bindir}/tcxmlcheck
%attr(755,root,root) %{_bindir}/tcxpm2rgb
%attr(755,root,root) %{_bindir}/tcyait
%attr(755,root,root) %{_bindir}/transcode
%dir %{_libdir}/%{name}
%attr(755,root,root) %{_libdir}/%{name}/a52_decore.so
%{_libdir}/%{name}/xvid4.cfg
%{_mandir}/man1/avifix.1*
%{_mandir}/man1/aviindex.1*
%{_mandir}/man1/avimerge.1*
%{_mandir}/man1/avisplit.1*
%{_mandir}/man1/avisync.1*
%{_mandir}/man1/tccat.1*
%{_mandir}/man1/tcdecode.1*
%{_mandir}/man1/tcdemux.1*
%{_mandir}/man1/tcexport.1*
%{_mandir}/man1/tcextract.1*
%{_mandir}/man1/tcmodchain.1*
%{_mandir}/man1/tcmodinfo.1*
%{_mandir}/man1/tcprobe.1*
%{_mandir}/man1/tcpvmexportd.1*
%{_mandir}/man1/tcscan.1*
%{_mandir}/man1/tcxmlcheck.1*
%{_mandir}/man1/transcode.1*
%{_mandir}/man1/transcode_export.1*
%{_mandir}/man1/transcode_filter.1*
%{_mandir}/man1/transcode_import.1*

%files avilib
%defattr(644,root,root,755)
%doc avilib/README.avilib
%{_includedir}/avilib.h

%files export
%defattr(644,root,root,755)
%attr(755,root,root) %{_libdir}/%{name}/export_*.so

%files import
%defattr(644,root,root,755)
%attr(755,root,root) %{_libdir}/%{name}/import_*.so

%files filter
%defattr(644,root,root,755)
%attr(755,root,root) %{_libdir}/%{name}/filter_*.so
%attr(755,root,root) %{_libdir}/%{name}/filter_list.awk
%attr(755,root,root) %{_libdir}/%{name}/parse_csv.awk
