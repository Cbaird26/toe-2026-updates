
import pandas as pd, numpy as np, json, os
from scipy.optimize import least_squares
import matplotlib.pyplot as plt

massmodel_path='MassModels_Lelli2016c.mrt'
btfr_path='BTFR_Lelli2019.mrt'

colspecs_mass=[(0,11),(12,18),(19,25),(26,32),(33,38),(39,45),(46,52),(53,59),(60,67),(68,76)]
names_mass=['ID','D','R','Vobs','e_Vobs','Vgas','Vdisk','Vbul','SBdisk','SBbul']
df=pd.read_fwf(massmodel_path,skiprows=25,colspecs=colspecs_mass,names=names_mass)

colspecs_btfr=[(0,12),(12,18),(18,24),(24,30),(30,36),(36,42),(42,48),(48,54),(54,60),(60,66),(66,72),(72,78),(78,84),(84,90),(90,96),(96,102),(102,108),(108,114),(114,120)]
names_btfr=['Name','logMb','e_logMb','Inc','e_Inc','Vf','e_Vf','V2exp','e_V2exp','V2eff','e_V2eff','Vmax','e_Vmax','Wp20','e_Wp20','Wm50','e_Wm50','Wm50c','e_Wm50c']
btf=pd.read_fwf(btfr_path, skiprows=30, colspecs=colspecs_btfr, names=names_btfr)

def vhalo2(r, vinf, rc):
    r=np.asarray(r, dtype=float)
    if rc < 1e-12:
        return np.full_like(r, vinf**2)
    return vinf**2 * (1.0 - (rc/np.maximum(r,1e-12))*np.arctan(r/rc))

def fit_baryon_only(g):
    r=g['R'].values; vobs=g['Vobs'].values; err=np.where(g['e_Vobs'].values>0,g['e_Vobs'].values,1.0)
    Vgas=g['Vgas'].values; Vdisk=g['Vdisk'].values; Vbul=g['Vbul'].values
    has_bul=(np.max(np.abs(Vbul))>1e-8)
    if has_bul:
        def res(p):
            yD,yB=p
            Vbar2=Vgas**2 + yD*Vdisk**2 + yB*Vbul**2
            return (np.sqrt(np.maximum(Vbar2,0))-vobs)/err
        p0=[0.5,0.7]; bounds=([0,0],[2,2])
    else:
        def res(p):
            yD=p[0]
            Vbar2=Vgas**2 + yD*Vdisk**2
            return (np.sqrt(np.maximum(Vbar2,0))-vobs)/err
        p0=[0.5]; bounds=([0],[2])
    out=least_squares(res,p0,bounds=bounds,max_nfev=20000)
    if has_bul:
        yD,yB=out.x
    else:
        yD=out.x[0]; yB=0.0
    Vbar2=Vgas**2 + yD*Vdisk**2 + yB*Vbul**2
    wrms=float(np.sqrt(np.mean((np.sqrt(np.maximum(Vbar2,0))-vobs)**2)))
    chi2=float(np.sum(res(out.x)**2)); dof=max(len(r)-len(out.x),1)
    return {'yD':float(yD),'yB':float(yB),'chi2_red':chi2/dof,'wrms':wrms,'k':len(out.x)}

def fit_halo(g):
    r=g['R'].values; vobs=g['Vobs'].values; err=np.where(g['e_Vobs'].values>0,g['e_Vobs'].values,1.0)
    Vgas=g['Vgas'].values; Vdisk=g['Vdisk'].values; Vbul=g['Vbul'].values
    has_bul=(np.max(np.abs(Vbul))>1e-8)
    if has_bul:
        def res(p):
            yD,yB,vinf,rc=p
            Vbar2=Vgas**2 + yD*Vdisk**2 + yB*Vbul**2
            v=np.sqrt(np.maximum(Vbar2 + vhalo2(r,vinf,rc),0))
            return (v-vobs)/err
        p0=[0.5,0.7,max(vobs.max()/2,5),max(np.median(r),0.5)]
        bounds=([0,0,0.1,1e-3],[2,2,500,1e3])
    else:
        def res(p):
            yD,vinf,rc=p
            Vbar2=Vgas**2 + yD*Vdisk**2
            v=np.sqrt(np.maximum(Vbar2 + vhalo2(r,vinf,rc),0))
            return (v-vobs)/err
        p0=[0.5,max(vobs.max()/2,5),max(np.median(r),0.5)]
        bounds=([0,0.1,1e-3],[2,500,1e3])
    out=least_squares(res,p0,bounds=bounds,max_nfev=30000)
    if has_bul:
        yD,yB,vinf,rc=out.x
    else:
        yD,vinf,rc=out.x; yB=0.0
    Vbar2=Vgas**2 + yD*Vdisk**2 + yB*Vbul**2
    v=np.sqrt(np.maximum(Vbar2 + vhalo2(r,vinf,rc),0))
    wrms=float(np.sqrt(np.mean((v-vobs)**2)))
    chi2=float(np.sum(res(out.x)**2)); dof=max(len(r)-len(out.x),1)
    return {'yD':float(yD),'yB':float(yB),'vinf':float(vinf),'rc_kpc':float(rc),'chi2_red':chi2/dof,'wrms':wrms,'k':len(out.x)}

results=[]
for gid,g in df.groupby('ID'):
    rb=fit_baryon_only(g)
    rh=fit_halo(g)
    results.append({
        'ID':gid,'n_points':len(g),
        'yD_bary':rb['yD'],'yB_bary':rb['yB'],'chi2_red_bary':rb['chi2_red'],'wrms_bary_kms':rb['wrms'],
        'yD_halo':rh['yD'],'yB_halo':rh['yB'],'vinf_kms':rh['vinf'],'rc_kpc':rh['rc_kpc'],
        'chi2_red_halo':rh['chi2_red'],'wrms_halo_kms':rh['wrms'],
        'wrms_improvement_kms':rb['wrms']-rh['wrms']
    })
resdf=pd.DataFrame(results).sort_values('ID')
resdf.to_csv('scalar_halo_fit_results.csv',index=False)

summary_all={
    'galaxies_total': int(len(resdf)),
    'median_wrms_bary_all': float(resdf['wrms_bary_kms'].median()),
    'median_wrms_halo_all': float(resdf['wrms_halo_kms'].median()),
}
with open('scalar_halo_summary.json','w') as f:
    json.dump(summary_all,f,indent=2)
print('Done.')
