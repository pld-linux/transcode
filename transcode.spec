Summary:	converter
Summary(pl):	converter
Name:		transcode
Version:	0.5.0
Release:	1
License:	GPL
Group:		Applications
Source0:	%{name}-%{version}.tgz
URL:		http://
BuildRequires:	avifile-devel
BuildRequires:	quicktime-devel
BuildRequires:	libdv-devel
BuildRequires:	libmpeg3-devel
BuildRequires:	libdvdread-devel
BuildRequires:	lame-libs-devel
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%description
N/A

%description -l pl
N/A

%prep
%setup  -q

%build
%configure
%{__make}

%install
rm -rf $RPM_BUILD_ROOT

%{__make} install DESTDIR=$RPM_BUILD_ROOT

gzip -9nf README ChangeLog

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr(644,root,root,755)
