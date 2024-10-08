"""Functions for 'clean' stage of CMACBench dataset"""
import logging
import shutil

from . import constants


logger = logging.getLogger(__name__)


def clean(dry_run=True):
    """Removes all generated directories:
    CMACBench and DATA_WE_CANT_SHARE"""
    logger.info(
        f"Removing DATASET_ROOT: {constants.DATASET_ROOT}"
    )
    if not dry_run:
        shutil.rmtree(constants.DATASET_ROOT)
