-- UPADTE: include FLAGS, limit magnitude of 21 mag per band
-- output on easyaccess web: Y3A2_COADD_SUMMARY_mag21_extwavg_flags.fits
select y3a2.coadd_object_id,
       y3a2.imaflags_iso_g imaflags_iso_g,
       y3a2.imaflags_iso_r imaflags_iso_r,
       y3a2.imaflags_iso_i imaflags_iso_i,
       y3a2.imaflags_iso_z imaflags_iso_z,
       y3a2.imaflags_iso_Y imaflags_iso_Y,
       y3a2.flags_g flags_g,
       y3a2.flags_r flags_r,
       y3a2.flags_i flags_i,
       y3a2.flags_z flags_z,
       y3a2.flags_Y flags_Y,
       xt.EXT_WAVG ext_wavg,
       g.mag_auto g_mag_auto,
       r.mag_auto r_mag_auto,
       i.mag_auto i_mag_auto,
       z.mag_auto z_mag_auto,
       Y.mag_auto Y_mag_auto,
       g.mag_petro g_mag_petro,
       r.mag_petro r_mag_petro,
       i.mag_petro i_mag_petro,
       z.mag_petro z_mag_petro,
       Y.mag_petro Y_mag_petro,
       g.mag_aper_1 g_mag_aper_1, g.mag_aper_2 g_mag_aper_2, g.mag_aper_3 g_mag_aper_3,
       g.mag_aper_4 g_mag_aper_4, g.mag_aper_5 g_mag_aper_5, g.mag_aper_6 g_mag_aper_6,
       g.mag_aper_7 g_mag_aper_7, g.mag_aper_8 g_mag_aper_8, g.mag_aper_9 g_mag_aper_9,
       g.mag_aper_10 g_mag_aper_10, g.mag_aper_11 g_mag_aper_11, g.mag_aper_12 g_mag_aper_12,
       r.mag_aper_1 r_mag_aper_1, r.mag_aper_2 r_mag_aper_2, r.mag_aper_3 r_mag_aper_3,
       r.mag_aper_4 r_mag_aper_4, r.mag_aper_5 r_mag_aper_5, r.mag_aper_6 r_mag_aper_6,
       r.mag_aper_7 r_mag_aper_7, r.mag_aper_8 r_mag_aper_8, r.mag_aper_9 r_mag_aper_9,
       r.mag_aper_10 r_mag_aper_10, r.mag_aper_11 r_mag_aper_11, r.mag_aper_12 r_mag_aper_12,
       i.mag_aper_1 i_mag_aper_1, i.mag_aper_2 i_mag_aper_2, i.mag_aper_3 i_mag_aper_3,
       i.mag_aper_4 i_mag_aper_4, i.mag_aper_5 i_mag_aper_5, i.mag_aper_6 i_mag_aper_6,
       i.mag_aper_7 i_mag_aper_7, i.mag_aper_8 i_mag_aper_8, i.mag_aper_9 i_mag_aper_9,
       i.mag_aper_10 i_mag_aper_10, i.mag_aper_11 i_mag_aper_11, i.mag_aper_12 i_mag_aper_12,
       z.mag_aper_1 z_mag_aper_1, z.mag_aper_2 z_mag_aper_2, z.mag_aper_3 z_mag_aper_3,
       z.mag_aper_4 z_mag_aper_4, z.mag_aper_5 z_mag_aper_5, z.mag_aper_6 z_mag_aper_6,
       z.mag_aper_7 z_mag_aper_7, z.mag_aper_8 z_mag_aper_8, z.mag_aper_9 z_mag_aper_9,
       z.mag_aper_10 z_mag_aper_10, z.mag_aper_11 z_mag_aper_11, z.mag_aper_12 z_mag_aper_12,
       Y.mag_aper_1 Y_mag_aper_1, Y.mag_aper_2 Y_mag_aper_2, Y.mag_aper_3 Y_mag_aper_3,
       Y.mag_aper_4 Y_mag_aper_4, Y.mag_aper_5 Y_mag_aper_5, Y.mag_aper_6 Y_mag_aper_6,
       Y.mag_aper_7 Y_mag_aper_7, Y.mag_aper_8 Y_mag_aper_8, Y.mag_aper_9 Y_mag_aper_9,
       Y.mag_aper_10 Y_mag_aper_10, Y.mag_aper_11 Y_mag_aper_11, Y.mag_aper_12 Y_mag_aper_12,
       y3a2.wavg_mag_psf_g g_wavg_mag_psf,
       y3a2.wavg_mag_psf_r r_wavg_mag_psf,
       y3a2.wavg_mag_psf_i i_wavg_mag_psf,
       y3a2.wavg_mag_psf_z z_wavg_mag_psf,
       y3a2.wavg_mag_psf_y Y_wavg_mag_psf
from (select coadd_object_id
  from y3a2_coadd_object_summary sample(5)
  where mag_auto_g < 21
    and mag_auto_r < 21
    and mag_auto_i < 21
    and mag_auto_z < 21
    and mag_auto_Y < 21
  ) suby3
join y3a2_coadd_object_band_g g on g.coadd_object_id=suby3.coadd_object_id
join y3a2_coadd_object_band_r r on r.coadd_object_id=suby3.coadd_object_id
join y3a2_coadd_object_band_i i on i.coadd_object_id=suby3.coadd_object_id
join y3a2_coadd_object_band_z z on z.coadd_object_id=suby3.coadd_object_id
join y3a2_coadd_object_band_Y Y on Y.coadd_object_id=suby3.coadd_object_id
join BECHTOL.Y3A2_EXT_MASH_V2 xt on xt.coadd_object_id=suby3.coadd_object_id
join y3a2_coadd_object_summary y3a2 on y3a2.coadd_object_id=suby3.coadd_object_id;
