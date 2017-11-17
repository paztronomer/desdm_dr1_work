--
-- Select the aperture fluxes, fwhm, mag_auto_i, flux_radius, kron_radius, petro_radius
--
select y3a2.coadd_object_id,
       xt.EXT_WAVG ext_wavg,
       g.mag_auto g_mag_auto,
       g.fwhmpsf_image g_fwhmpsf_image, g.fwhm_image g_fwhm_image,
       g.flux_radius g_flux_radius, g.kron_radius g_kron_radius, g.petro_radius g_petro_radius,      r.mag_auto r_mag_auto,
       r.fwhmpsf_image r_fwhmpsf_image, r.fwhm_image r_fwhm_image,
       r.flux_radius r_flux_radius, r.kron_radius r_kron_radius, r.petro_radius r_petro_radius,
       i.mag_auto i_mag_auto,
       i.fwhmpsf_image i_fwhmpsf_image, i.fwhm_image i_fwhm_image,
       i.flux_radius i_flux_radius, i.kron_radius i_kron_radius, i.petro_radius i_petro_radius,
       z.mag_auto z_mag_auto,
       z.fwhmpsf_image z_fwhmpsf_image, z.fwhm_image z_fwhm_image,
       z.flux_radius z_flux_radius, z.kron_radius z_kron_radius, z.petro_radius z_petro_radius,
       Y.mag_auto Y_mag_auto,
       Y.fwhmpsf_image Y_fwhmpsf_image, Y.fwhm_image Y_fwhm_image,
       Y.flux_radius Y_flux_radius, Y.kron_radius Y_kron_radius, Y.petro_radius Y_petro_radius,
       g.flux_aper_1 g_flux_aper_1, g.flux_aper_2 g_flux_aper_2, g.flux_aper_3 g_flux_aper_3,
       g.flux_aper_4 g_flux_aper_4, g.flux_aper_5 g_flux_aper_5, g.flux_aper_6 g_flux_aper_6,
       g.flux_aper_7 g_flux_aper_7, g.flux_aper_8 g_flux_aper_8, g.flux_aper_9 g_flux_aper_9,
       g.flux_aper_10 g_flux_aper_10, g.flux_aper_11 g_flux_aper_11, g.flux_aper_12 g_flux_aper_12,
       r.flux_aper_1 r_flux_aper_1, r.flux_aper_2 r_flux_aper_2, r.flux_aper_3 r_flux_aper_3,
       r.flux_aper_4 r_flux_aper_4, r.flux_aper_5 r_flux_aper_5, r.flux_aper_6 r_flux_aper_6,
       r.flux_aper_7 r_flux_aper_7, r.flux_aper_8 r_flux_aper_8, r.flux_aper_9 r_flux_aper_9,
       r.flux_aper_10 r_flux_aper_10, r.flux_aper_11 r_flux_aper_11, r.flux_aper_12 r_flux_aper_12,
       i.flux_aper_1 i_flux_aper_1, i.flux_aper_2 i_flux_aper_2, i.flux_aper_3 i_flux_aper_3,
       i.flux_aper_4 i_flux_aper_4, i.flux_aper_5 i_flux_aper_5, i.flux_aper_6 i_flux_aper_6,
       i.flux_aper_7 i_flux_aper_7, i.flux_aper_8 i_flux_aper_8, i.flux_aper_9 i_flux_aper_9,
       i.flux_aper_10 i_flux_aper_10, i.flux_aper_11 i_flux_aper_11, i.flux_aper_12 i_flux_aper_12,
       z.flux_aper_1 z_flux_aper_1, z.flux_aper_2 z_flux_aper_2, z.flux_aper_3 z_flux_aper_3,
       z.flux_aper_4 z_flux_aper_4, z.flux_aper_5 z_flux_aper_5, z.flux_aper_6 z_flux_aper_6,
       z.flux_aper_7 z_flux_aper_7, z.flux_aper_8 z_flux_aper_8, z.flux_aper_9 z_flux_aper_9,
       z.flux_aper_10 z_flux_aper_10, z.flux_aper_11 z_flux_aper_11, z.flux_aper_12 z_flux_aper_12,
       Y.flux_aper_1 Y_flux_aper_1, Y.flux_aper_2 Y_flux_aper_2, Y.flux_aper_3 Y_flux_aper_3,
       Y.flux_aper_4 Y_flux_aper_4, Y.flux_aper_5 Y_flux_aper_5, Y.flux_aper_6 Y_flux_aper_6,
       Y.flux_aper_7 Y_flux_aper_7, Y.flux_aper_8 Y_flux_aper_8, Y.flux_aper_9 Y_flux_aper_9,
       Y.flux_aper_10 Y_flux_aper_10, Y.flux_aper_11 Y_flux_aper_11, Y.flux_aper_12 Y_flux_aper_12
from (select coadd_object_id
  from y3a2_coadd_object_summary sample(15)
  where mag_auto_i < 22.5
  ) y3
join y3a2_coadd_object_band_g g on g.coadd_object_id=y3.coadd_object_id
join y3a2_coadd_object_band_r r on r.coadd_object_id=y3.coadd_object_id
join y3a2_coadd_object_band_i i on i.coadd_object_id=y3.coadd_object_id
join y3a2_coadd_object_band_z z on z.coadd_object_id=y3.coadd_object_id
join y3a2_coadd_object_band_Y Y on Y.coadd_object_id=y3.coadd_object_id
join BECHTOL.Y3A2_EXT_MASH_V2 xt on xt.coadd_object_id=y3.coadd_object_id
join y3a2_coadd_object_summary y3a2 on y3a2.coadd_object_id=y3.coadd_object_id;
