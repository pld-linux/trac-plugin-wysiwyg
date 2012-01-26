%define		trac_ver	0.12
%define		plugin		wysiwyg
Summary:	Wysiwyg Plugin for Trac
Name:		trac-plugin-%{plugin}
Version:	%{trac_ver}.0.4
Release:	1
License:	BSD
Group:		Applications/WWW
Source0:	http://trac-hacks.org/changeset/latest/tracwysiwygplugin?old_path=/&filename=%{plugin}-%{version}&format=zip#/%{plugin}-%{version}.zip
# Source0-md5:	765d663662c141944b3ab1125cb2ff68
URL:		http://trac-hacks.org/wiki/TracWysiwygPlugin
BuildRequires:	python-devel
BuildRequires:	python-modules
BuildRequires:	python-setuptools
BuildRequires:	rpm-pythonprov
BuildRequires:	unzip
Requires:	trac >= %{trac_ver}
# for htdocs alias, can be removed in 0.13
Requires:	trac >= 0.12.2-4
BuildArch:	noarch
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%define		trac_htdocs	/usr/share/trac/htdocs

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

# - one of my trac installs failed to load htdocs data and had to make such alias in apache config:
# AliasMatch ^/trac/[^/]+/chrome/tracwysiwyg/(.*) %{_datadir}/python2.6/site-packages/tracwysiwyg/htdocs/$1
# mv htdocs, so extra alias won't be needed
install -d $RPM_BUILD_ROOT%{trac_htdocs}
mv $RPM_BUILD_ROOT{%{py_sitescriptdir}/trac%{plugin}/htdocs,%{trac_htdocs}/trac%{plugin}}

%py_postclean

%clean
rm -rf $RPM_BUILD_ROOT

%post
trac-enableplugin tracwysiwyg.WysiwygModule

%files
%defattr(644,root,root,755)
%{py_sitescriptdir}/trac%{plugin}
%{py_sitescriptdir}/TracWysiwyg-%{version}-py*.egg-info
%{trac_htdocs}/trac%{plugin}
