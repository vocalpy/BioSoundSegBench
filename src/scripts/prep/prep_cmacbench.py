import logging
import sys
from typing import Literal

import cmacbench

# ---- typehint
Stage = Literal[
    "all", "clean", "mkdirs", "copy", "labels", "qc", "make", "split"
]


logger = logging.getLogger('biosoundsegbench')  # 'base' logger
formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
stream_handler = logging.StreamHandler(sys.stdout)
stream_handler.setFormatter(formatter)
logger.addHandler(stream_handler)
logger.setLevel('INFO')



def prep_biosoundsegbench(
        stage: Stage = 'all',
        biosound_groups: list = cmacbench.prep.constants.BIOSOUND_GROUPS,
        dry_run: bool = True,
):
    """Main function that prepares BioSoundSegBench dataset"""
    logger.info(
        "Preparing BioSoundSegBench dataset.\n"
        f"Stage: {stage}\n"
        f"Dry run: {dry_run}\n"
    )
    if stage == "clean":
        logger.info(
            "Stage was 'clean', will remove BioSoundSegBench directory and return."
        )
        cmacbench.prep.clean(dry_run)
        return

    if stage =='mkdirs' or stage == 'all':
        logger.info(
            f"Stage was '{stage}', will make directories for BioSoundSegBench dataset."
        )
        # ---- make all the directories
        cmacbench.prep.mkdirs(dry_run)

    if stage =='copy' or stage == 'all':
        logger.info(
            f"Stage was '{stage}', will copy raw audio into BioSoundSegBench dataset, and copy/convert/generate annotations as needed."
        )
        # ---- copy the raw audio, copy/convert/generate annotations
        cmacbench.prep.copy_audio_copy_make_annot_all(biosound_groups, dry_run)

    if stage =='labels' or stage == 'all':
        logger.info(
            f"Stage was '{stage}', will make metadata for class labels."
        )
        cmacbench.prep.make_labelsets_and_labelmaps(dry_run)

    if stage =='qc' or stage == 'all':
        logger.info(
            f"Stage was '{stage}', will do quality checks on annotations and remove invalid audio/annotation pairs."
        )
        cmacbench.prep.do_qc(biosound_groups, dry_run)

    if stage =='make' or stage == 'all':
        logger.info(
            f"Stage was '{stage}', will make inputs and targets for neural network models."
        )
        # ---- make frames + frame classification, boundary detection vectors
        cmacbench.prep.make_inputs_and_targets_all(biosound_groups, dry_run)

    if stage =='split' or stage == 'all':
        logger.info(
            f"Stage was '{stage}', will make csv files representing dataset splits."
        )
        # ---- make frames + frame classification, boundary detection vectors
        cmacbench.prep.make_splits_all(biosound_groups, dry_run)


parser = cmacbench.prep.parser.get_parser()
args = parser.parse_args()

prep_biosoundsegbench(
    stage=args.stage,
    biosound_groups=args.biosound_groups,
    dry_run=args.dry_run,
)
