Name: ocd-release
Version: 3.4
Release: 20190324%{?dist}
Summary: OCD OS Release Information
License: GPLv2
Group: System Environment/Base
Vendor: The Linux Community/LLNL
Source: %{name}-%{version}.tgz
BuildRoot: %{_tmppath}/%{name}-%{version}
BuildArch: noarch
Requires: rpm coreutils
%define __spec_install_post /usr/lib/rpm/brp-compress || :
%define  debug_package   %{nil}

%description
OCD

%package base
Summary: base
Group: System Environment/Base
Requires: ocd-release
%description base
base
%files base
/usr/share/doc/%{name}-%{version}/base

%prep
%setup -q -n %{name}-%{version}

%build

%install
%{__mkdir_p} %{buildroot}/etc/ocd 
%{__mkdir_p} %{buildroot}/usr/share/doc/%{name}-%{version} 
%{__mkdir_p} %{buildroot}/etc/yum.repos.d

echo base         > %{buildroot}/usr/share/doc/%{name}-%{version}/base

%{__install} -m 444 rpmlist_*   %{buildroot}/etc/ocd
%{__install} -m 444 LICENSE     %{buildroot}/usr/share/doc/%{name}-%{version}/
%{__install} -m 444 NOTICE      %{buildroot}/usr/share/doc/%{name}-%{version}/
%{__install} -m 444 README      %{buildroot}/usr/share/doc/%{name}-%{version}/
%{__install} -m 644 ocd.repo    %{buildroot}/etc/yum.repos.d/ocd.repo
echo "%{name}-%{version}-%{release}" | sed s/\.ocd3.*// > %{buildroot}/etc/ocd-release
chmod 444 %{buildroot}/etc/ocd-release

# Install CR/LF Builder key
%{__mkdir_p} %{buildroot}/etc/pki/rpm-gpg
%{__mkdir_p} %{buildroot}/etc/pki/rpm-gpg/CentOS
%{__cp} keys/RPM-GPG-KEY* $RPM_BUILD_ROOT/etc/pki/rpm-gpg
%{__cp} keys/CentOS/RPM-GPG-KEY* $RPM_BUILD_ROOT/etc/pki/rpm-gpg/CentOS

# link in correct opt rpmlist
cd %{buildroot}/etc/ocd 
rm -f rpmlist_base rpmlist_minimal
ln -s rpmlist_base_`arch` rpmlist_base
ln -s rpmlist_minimal_`arch` rpmlist_minimal

%clean
rm -rf %{buildroot}

%files 
%defattr(-,root,root,0555)
%attr(0755,root,root) %dir /etc/ocd
%defattr(-,root,root,0444)
/etc/ocd/rpmlist_*
/etc/ocd-release
%config(noreplace) /etc/yum.repos.d/ocd.repo
/usr/share/doc/%{name}-%{version}/LICENSE
/usr/share/doc/%{name}-%{version}/NOTICE
/usr/share/doc/%{name}-%{version}/README
/etc/pki/rpm-gpg/RPM-GPG-KEY*
/etc/pki/rpm-gpg/CentOS/RPM-GPG-KEY*

%post
# install all the public keys
rpm --import /etc/pki/rpm-gpg/RPM-GPG-KEY*
rpm --import /etc/pki/rpm-gpg/CentOS/RPM-GPG-KEY*

# link in correct opt rpmlist
cd /etc/ocd 
rm -f rpmlist_base rpmlist_minimal
ln -s rpmlist_base_`arch` rpmlist_base
ln -s rpmlist_minimal_`arch` rpmlist_minimal
