# Scalar-halo SWELLS multi-object pilot (reconstructed)

This file was reconstructed from the in-chat reported results because the original artifact was no longer present on disk.

## Sample-level summary
Using a 15-object SWELLS spiral-lens pilot:

### Exact BTFR baseline
- median predicted/observed Einstein-radius ratio = 0.122
- median absolute fractional error = 0.878
- fraction within 20% = 0.133
- zero-Einstein predictions = 7/15

### Global compromise model
Using a single global adjustment with:
- core ratio kappa = 0.5
- scalar amplitude multiplier s = 1.5

Results:
- median predicted/observed Einstein-radius ratio = 1.029
- median absolute fractional error = 0.184
- fraction within 20% = 0.60
- zero-Einstein predictions = 2/15

## Reported outliers under the compromise model
- J1703+2451: no finite Einstein radius
- J1331+3638: no finite Einstein radius
- J0955+0101: predicted 0.47 arcsec vs observed 1.04 arcsec
- J0915+4211: predicted 1.39 arcsec vs observed 0.98 arcsec
- J0841+3824: predicted 1.06 arcsec vs observed 1.46 arcsec

## Note
This reconstructed package preserves the reported metrics and named outliers, but not the full original per-object table, which was unavailable.
