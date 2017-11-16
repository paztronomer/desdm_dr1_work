--
-- Select the aperture fluxes, fwhm, mag_auto_i, mag_radius, kron_radius, petro_radius
--
select dr1.coadd_object_id,
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
       dr1.wavg_mag_psf_g g_wavg_mag_psf,
       dr1.wavg_mag_psf_r r_wavg_mag_psf,
       dr1.wavg_mag_psf_i i_wavg_mag_psf,
       dr1.wavg_mag_psf_z z_wavg_mag_psf,
       dr1.wavg_mag_psf_y Y_wavg_mag_psf
from (select coadd_object_id
  from dr1_main sample(15)
  where mag_auto_i < 22.5
  ) y3
join dr1_band_g g on g.coadd_object_id=y3.coadd_object_id
join dr1_band_r r on r.coadd_object_id=y3.coadd_object_id
join dr1_band_i i on i.coadd_object_id=y3.coadd_object_id
join dr1_band_z z on z.coadd_object_id=y3.coadd_object_id
join dr1_band_Y Y on Y.coadd_object_id=y3.coadd_object_id
join dr1_main dr1 on dr1.coadd_object_id=y3.coadd_object_id;
