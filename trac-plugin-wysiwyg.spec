# TODO
# - one of my trac installs failed to load htdocs data and had to make such alias in apache config:
#   AliasMatch ^/trac/[^/]+/chrome/tracwysiwyg/(.*) /usr/share/python2.6/site-packages/tracwysiwyg/htdocs/$1
%define		trac_ver	0.12
%define		rev		7817
%define		plugin		wysiwyg
Summary:	Wysiwyg Plugin for Trac
Name:		trac-plugin-%{plugin}
Version:	%{trac_ver}.0.2
Release:	1
License:	BSD
Group:		Applications/WWW
Source0:	http://trac-hacks.org/changeset/latest/tracwysiwygplugin?old_path=/&filename=%{plugin}-%{version}&format=zip#/%{plugin}-%{version}.zip
# Source0-md5:	a6b46da0a6078c6988dc3d0d36f81ce6
URL:		http://trac-hacks.org/wiki/TracWysiwygPlugin
BuildRequires:	python-devel
BuildRequires:	python-modules
BuildRequires:	rpm-pythonprov
BuildRequires:	unzip
Requires:	trac >= %{trac_ver}
BuildArch:	noarch
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%description
Wysiwyg editor embedded into textarea.wikitext.

%prep
%setup -qc
mv trac%{plugin}plugin/%{trac_ver}/* .

%build
%{__python} setup.py build
%{__python} setup.py egg_info

ver=$(awk '$1 == "Version:" {print $2}' *.egg-info/PKG-INFO)
test "$ver" = %{version}

%install
rm -rf $RPM_BUILD_ROOT
%{__python} setup.py install \
	--single-version-externally-managed \
	--optimize 2 \
	--root=$RPM_BUILD_ROOT

%py_postclean

%clean
rm -rf $RPM_BUILD_ROOT

%post
trac-enableplugin tracwysiwyg.WysiwygModule

%files
%defattr(644,root,root,755)
%{py_sitescriptdir}/trac%{plugin}
%{py_sitescriptdir}/TracWysiwyg-%{version}-py*.egg-info
