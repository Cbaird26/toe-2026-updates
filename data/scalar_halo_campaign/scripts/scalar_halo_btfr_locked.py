import pandas as pd, numpy as np, json
from scipy.optimize import least_squares
import matplotlib.pyplot as plt

massmodel_path='/mnt/data/MassModels_Lelli2016c.mrt'
btfr_path='/mnt/data/BTFR_Lelli2019.mrt'
first_pass_path='/mnt/data/scalar_halo_fit_results.csv'
G_kpc_kms = 4.30091e-6
c_kms = 299792.458

colspecs_mass=[(0,11),(12,18),(19,25),(26,32),(33,38),(39,45),(46,52),(53,59),(60,67),(68,76)]
names_mass=['ID','D','R','Vobs','e_Vobs','Vgas','Vdisk','Vbul','SBdisk','SBbul']
df=pd.read_fwf(massmodel_path,skiprows=25,colspecs=colspecs_mass,names=names_mass)
df['ID']=df['ID'].str.strip()
colspecs_btfr=[(0,12),(12,18),(18,24),(24,30),(30,36),(36,42),(42,48)]
names_btfr=['Name','logMb','e_logMb','Inc','e_Inc','Vf','e_Vf']
bt=pd.read_fwf(btfr_path, skiprows=30,colspecs=colspecs_btfr,names=names_btfr)
bt['Name']=bt['Name'].str.strip()
mb_map=bt.set_index('Name')['logMb'].to_dict()
first=pd.read_csv(first_pass_path)
first['ID']=first['ID'].str.strip()

# From outer-loop search already performed in-session
BEST_FREE = {'V0_kms': 122.0, 'p': 0.24, 'median_chi2_red': 1.9085561421071853, 'median_wrms': 5.6748846162010045}
BEST_BTFR = {'V0_kms': 120.0, 'p': 0.25, 'median_chi2_red': 1.9897890071101565, 'median_wrms': 5.709140794372944}


def vhalo2(r, vinf, rc):
    r=np.asarray(r, dtype=float)
    return vinf**2 * (1.0 - (rc/np.maximum(r,1e-12))*np.arctan(r/rc))

def fit_baryon_only(g):
    r=g['R'].values; vobs=g['Vobs'].values; err=np.where(g['e_Vobs'].values>0,g['e_Vobs'].values,1.0)
    Vgas=g['Vgas'].values; Vdisk=g['Vdisk'].values; Vbul=g['Vbul'].values
    has_bul=(np.max(np.abs(Vbul))>1e-8)
    if has_bul:
        def res(p):
            yD,yB=p
            v=np.sqrt(np.maximum(Vgas**2 + yD*Vdisk**2 + yB*Vbul**2,0))
            return (v-vobs)/err
        p0=[0.5,0.7]; bounds=([0,0],[2,2])
    else:
        def res(p):
            yD=p[0]
            v=np.sqrt(np.maximum(Vgas**2 + yD*Vdisk**2,0))
            return (v-vobs)/err
        p0=[0.5]; bounds=([0],[2])
    out=least_squares(res,p0,bounds=bounds,max_nfev=1500)
    if has_bul:
        yD,yB=out.x
    else:
        yD=out.x[0]; yB=0.0
    v=np.sqrt(np.maximum(Vgas**2 + yD*Vdisk**2 + yB*Vbul**2,0))
    chi2=np.sum(res(out.x)**2); dof=max(len(r)-len(out.x),1)
    return {'yD':float(yD),'yB':float(yB),'chi2_red':float(chi2/dof),'wrms':float(np.sqrt(np.mean((v-vobs)**2))),'vmodel':v}

def fit_local_fixed_vinf(g, vinf):
    r=g['R'].values; vobs=g['Vobs'].values; err=np.where(g['e_Vobs'].values>0,g['e_Vobs'].values,1.0)
    Vgas=g['Vgas'].values; Vdisk=g['Vdisk'].values; Vbul=g['Vbul'].values
    has_bul=(np.max(np.abs(Vbul))>1e-8)
    rc0=max(np.median(r),0.5)
    if has_bul:
        def res(p):
            yD,yB,rc=p
            v=np.sqrt(np.maximum(Vgas**2 + yD*Vdisk**2 + yB*Vbul**2 + vhalo2(r,vinf,rc),0))
            return (v-vobs)/err
        p0=[0.5,0.7,rc0]; bounds=([0,0,1e-3],[2,2,1e3])
    else:
        def res(p):
            yD,rc=p
            v=np.sqrt(np.maximum(Vgas**2 + yD*Vdisk**2 + vhalo2(r,vinf,rc),0))
            return (v-vobs)/err
        p0=[0.5,rc0]; bounds=([0,1e-3],[2,1e3])
    out=least_squares(res,p0,bounds=bounds,max_nfev=1500)
    if has_bul:
        yD,yB,rc=out.x
    else:
        yD,rc=out.x; yB=0.0
    v=np.sqrt(np.maximum(Vgas**2 + yD*Vdisk**2 + yB*Vbul**2 + vhalo2(r,vinf,rc),0))
    chi2=np.sum(res(out.x)**2); dof=max(len(r)-len(out.x),1)
    return {'yD':float(yD),'yB':float(yB),'rc_kpc':float(rc),'chi2_red':float(chi2/dof),'wrms':float(np.sqrt(np.mean((v-vobs)**2))),'vmodel':v}

records=[]
for gid,g in df.groupby('ID'):
    gid=gid.strip()
    rec={'ID':gid,'n_points':len(g)}
    rb=fit_baryon_only(g)
    rec.update({'wrms_bary_kms':rb['wrms'],'chi2_red_bary':rb['chi2_red']})
    if gid in set(first['ID']):
        row=first[first['ID']==gid].iloc[0]
        rec.update({'wrms_free_kms':float(row['wrms_halo_kms']),'chi2_red_free':float(row['chi2_red_halo']),'vinf_free_kms':float(row['vinf_kms']),'rc_free_kpc':float(row['rc_kpc'])})
    if gid in mb_map:
        Mb=10**mb_map[gid]
        vinf_btfr=BEST_BTFR['V0_kms']*(Mb/1e10)**BEST_BTFR['p']
        vinf_freepred=BEST_FREE['V0_kms']*(Mb/1e10)**BEST_FREE['p']
        r_btfr=fit_local_fixed_vinf(g, vinf_btfr)
        r_freepred=fit_local_fixed_vinf(g, vinf_freepred)
        rec.update({
            'logMb':float(mb_map[gid]),
            'vinf_btfr_kms':float(vinf_btfr),'rc_btfr_kpc':r_btfr['rc_kpc'],'wrms_btfr_kms':r_btfr['wrms'],'chi2_red_btfr':r_btfr['chi2_red'],
            'vinf_freepred_kms':float(vinf_freepred),'rc_freepred_kpc':r_freepred['rc_kpc'],'wrms_freepred_kms':r_freepred['wrms'],'chi2_red_freepred':r_freepred['chi2_red']
        })
    records.append(rec)
res=pd.DataFrame(records).sort_values('ID')
res.to_csv('/mnt/data/scalar_halo_btfr_locked_results.csv',index=False)

matched10=res[(res['vinf_btfr_kms'].notna())&(res['n_points']>=10)].copy()
summary={
    'best_free_exponent_locked_model': BEST_FREE,
    'best_fixed_btfr_locked_model': BEST_BTFR,
    'matched_n_ge_10': int(len(matched10)),
    'median_wrms_bary_n_ge_10': float(matched10['wrms_bary_kms'].median()),
    'median_wrms_free_per_galaxy_n_ge_10': float(matched10['wrms_free_kms'].median()),
    'median_wrms_btfr_locked_n_ge_10': float(matched10['wrms_btfr_kms'].median()),
    'median_wrms_freepred_locked_n_ge_10': float(matched10['wrms_freepred_kms'].median()),
    'median_chi2_bary_n_ge_10': float(matched10['chi2_red_bary'].median()),
    'median_chi2_free_per_galaxy_n_ge_10': float(matched10['chi2_red_free'].median()),
    'median_chi2_btfr_locked_n_ge_10': float(matched10['chi2_red_btfr'].median()),
    'median_chi2_freepred_locked_n_ge_10': float(matched10['chi2_red_freepred'].median()),
    'frac_btfr_better_than_bary_n_ge_10': float((matched10['wrms_btfr_kms']<matched10['wrms_bary_kms']).mean()),
    'frac_btfr_within_35pct_of_free_n_ge_10': float((matched10['wrms_btfr_kms']<=1.35*matched10['wrms_free_kms']).mean()),
}
with open('/mnt/data/scalar_halo_btfr_locked_summary.json','w') as f:
    json.dump(summary,f,indent=2)

# Residual boxplot
fig,ax=plt.subplots(figsize=(8,5))
ax.boxplot([matched10['wrms_bary_kms'], matched10['wrms_free_kms'], matched10['wrms_btfr_kms']], labels=['Baryons','Free halo','BTFR-locked'], showfliers=False)
ax.set_ylabel('WRMS residual (km/s)')
ax.set_title('Matched SPARC sample (n>=10)')
ax.grid(alpha=0.25,axis='y')
plt.tight_layout(); plt.savefig('/mnt/data/scalar_halo_btfr_locked_residuals.png',dpi=180); plt.close(fig)

# Sample fits
sample_ids=['NGC2403','NGC3198','NGC6503','DDO154','UGC02885','F571-8']
fig,axs=plt.subplots(2,3,figsize=(14,8)); axs=axs.flatten()
for ax,gid in zip(axs,sample_ids):
    g=df[df['ID']==gid].copy()
    if g.empty or gid not in mb_map:
        ax.axis('off'); continue
    rb=fit_baryon_only(g)
    Mb=10**mb_map[gid]
    vinf_btfr=BEST_BTFR['V0_kms']*(Mb/1e10)**BEST_BTFR['p']
    rbt=fit_local_fixed_vinf(g, vinf_btfr)
    rfrow=first[first['ID']==gid].iloc[0]
    r=g['R'].values; Vgas=g['Vgas'].values; Vdisk=g['Vdisk'].values; Vbul=g['Vbul'].values
    v_free=np.sqrt(np.maximum(Vgas**2 + rfrow['yD_halo']*Vdisk**2 + rfrow['yB_halo']*Vbul**2 + vhalo2(r,rfrow['vinf_kms'],rfrow['rc_kpc']),0))
    ax.errorbar(g['R'],g['Vobs'],yerr=g['e_Vobs'],fmt='o',ms=3,color='black',alpha=0.8,label='obs')
    ax.plot(g['R'],rb['vmodel'],lw=2,color='#d95f02',label='baryons')
    ax.plot(g['R'],v_free,lw=2,color='#1b9e77',label='free halo')
    ax.plot(g['R'],rbt['vmodel'],lw=2,color='#7570b3',ls='--',label='BTFR-locked')
    ax.set_title(gid)
    ax.set_xlabel('R (kpc)'); ax.set_ylabel('V (km/s)'); ax.grid(alpha=0.2)
handles,labels=axs[0].get_legend_handles_labels()
fig.legend(handles,labels,loc='upper center',ncol=4,frameon=False)
plt.tight_layout(rect=[0,0,1,0.95]); plt.savefig('/mnt/data/scalar_halo_btfr_locked_sample_fits.png',dpi=180); plt.close(fig)

# BTFR diagnostics
obs=bt.merge(matched10[['ID']], left_on='Name', right_on='ID', how='inner')
obs=obs[obs['Vf']>0]
fig,ax=plt.subplots(figsize=(7,5))
ax.scatter(np.log10(obs['Vf']),obs['logMb'],s=18,color='black',alpha=0.65,label='observed flat speed')
ax.scatter(np.log10(matched10['vinf_btfr_kms']),matched10['logMb'],s=18,color='#7570b3',alpha=0.65,label='BTFR-locked scalar speed')
ax.scatter(np.log10(matched10['vinf_free_kms']),matched10['logMb'],s=18,color='#1b9e77',alpha=0.25,label='free per-galaxy scalar speed')
x=np.linspace(np.log10(matched10['vinf_btfr_kms'].min()*0.9),np.log10(matched10['vinf_btfr_kms'].max()*1.1),100)
y=10+(x-np.log10(BEST_BTFR['V0_kms']))/BEST_BTFR['p']
ax.plot(x,y,color='#7570b3',ls='--',lw=2,label='locked slope 4')
ax.set_xlabel('log10 speed (km/s)'); ax.set_ylabel('log10 baryonic mass (Msun)')
ax.set_title('Scalar-halo scaling diagnostics')
ax.grid(alpha=0.25); ax.legend(frameon=False,fontsize=8)
plt.tight_layout(); plt.savefig('/mnt/data/scalar_halo_btfr_locked_btfr_plot.png',dpi=180); plt.close(fig)

# Lensing reference table and quick formula check
R=np.linspace(0.1,30,200)
vinf=BEST_BTFR['V0_kms']; rc=3.0
rho = vinf**2/(4*np.pi*G_kpc_kms*(R**2+rc**2))
Sigma = vinf**2/(4*G_kpc_kms*np.sqrt(R**2+rc**2))
M2D = (np.pi*vinf**2/(2*G_kpc_kms))*(np.sqrt(R**2+rc**2)-rc)
alpha = 4*G_kpc_kms*M2D/(c_kms**2*np.maximum(R,1e-12))
pd.DataFrame({'R_kpc':R,'rho_Msun_per_kpc3':rho,'Sigma_Msun_per_kpc2':Sigma,'M2D_Msun':M2D,'alpha_rad':alpha}).to_csv('/mnt/data/scalar_halo_lensing_profile_reference.csv',index=False)

print('Done')
