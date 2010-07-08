# TODO
# - one of my trac installs failed to load htdocs data and had to make such alias in apache config:
#   AliasMatch ^/trac/[^/]+/chrome/tracwysiwyg/(.*) /usr/share/python2.6/site-packages/tracwysiwyg/htdocs/$1
%define		trac_ver	0.11
%define		rev		7817
%define		plugin		wysiwyg
Summary:	Wysiwyg Plugin for Trac
Name:		trac-plugin-%{plugin}
Version:	0.2
Release:	3
License:	BSD
Group:		Applications/WWW
Source0:	http://trac-hacks.org/changeset/%{rev}/tracwysiwygplugin?old_path=/&filename=tracwysiwygplugin&format=zip#/%{name}-%{version}-%{rev}.zip
# Source0-md5:	fbc0279bf41cc510e4e4766b2e5a3126
URL:		http://trac-hacks.org/wiki/TracWysiwygPlugin
BuildRequires:	python-devel
BuildRequires:	python-modules
BuildRequires:	rpm-pythonprov
BuildRequires:	unzip
Requires:	trac >= %{trac_ver}.7-3
BuildArch:	noarch
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%description
Wysiwyg editor embedded into textarea.wikitext.

%prep
%setup -q -n tracwysiwygplugin

%build
cd %{trac_ver}
%{__python} setup.py build
%{__python} setup.py egg_info

%install
rm -rf $RPM_BUILD_ROOT
cd %{trac_ver}
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
