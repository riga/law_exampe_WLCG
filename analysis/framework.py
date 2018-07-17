# -*- coding: utf-8 -*-

"""
Law example tasks to demonstrate job submission and remote storage on the WLCG.
For easier setup, run this example on lxplus.

In this file, some really basic tasks are defined that can be inherited by
other tasks to receive the same features. This is usually called "framework"
and only needs to be defined once per user / group / etc.
"""


__all__ = ["Task", "GridWorkflow"]


import os
import re

import law


# we are going to submit jobs to a GLite backend and store data on a WLCG storage element
# the implementations of the classes we need are part of law contrib packages which we need to load
law.contrib.load("glite")
law.contrib.load("wlcg")

# the grid jobs we want submit require our external software as well as the example code repository
# therefore, we will configure the jobs to transfer everything to a storage element, so the grid
# jobs can download it again before running (NOTE: we do not send software WITH each job here!)
# the upload is done by a dedicated task, while the download on the worker node is handled by the
# glite_bootstrap script
# we can use some helpers for bundling and file transfer (with replicas for scaling purposes) from
# law contrib packages
law.contrib.load("git", "tasks", "wlcg")


class Task(law.Task):
    """
    Base task that provides some convenience methods to create local and remote file at the default
    data store path.
    """

    def store_parts(self):
        return (self.__class__.__name__,)

    def local_path(self, *path):
        # WLCG_EXAMPLE_STORE is defined in setup.sh
        parts = [str(p) for p in self.store_parts() + path]
        return os.path.join(os.getenv("WLCG_EXAMPLE_STORE"), *parts)

    def local_target(self, *path):
        return law.LocalFileTarget(self.local_path(*path))

    def wlcg_path(self, *path):
        parts = [str(p) for p in self.store_parts() + path]
        return os.path.join(*parts)

    def wlcg_target(self, *args, **kwargs):
        # WLCG targets automatically read their configuation from the [wlcg_fs] config section
        # in case you want to use a different config (even in parallel), pass *config=<the_section>*
        # to this method and the resulting WLCG file target will use that config instead
        return law.WLCGFileTarget(self.wlcg_path(*args), **kwargs)


class GridWorkflow(law.GLiteWorkflow):
    """
    Here, we need to configure the default law.GLiteWorkflow to a minimal extent in order to send
    our bootstrap file and some variables to remote jobs. Law does not aim to auto-magically do this
    in a multi-purpose manner for all possible cases, but rather provides a simple interface to
    steer the exact behavior you want in your grid jobs.
    """

    def glite_output_directory(self):
        # the directory where submission meta data should be stored
        return law.LocalDirectoryTarget(self.local_path())

    def glite_create_job_file_factory(self):
        # tell the factory, which is responsible for creating our job files,
        # that the files are not temporary, i.e., it should not delete them after submission
        factory = super(GridWorkflow, self).glite_create_job_file_factory()
        factory.is_tmp = False
        return factory

    def glite_bootstrap_file(self):
        # each job can define a bootstrap file that is executed prior to the actual job
        # in order to setup software and environment variables
        return law.util.rel_path(__file__, "glite_bootstrap.sh")

    def glite_job_config(self, config, job_num, branches):
        # render_data is rendered into all files sent with a job, such as the glite_bootstrap file
        config.render_variables["grid_user"] = os.getenv("WLCG_EXAMPLE_GRID_USER")
        return config

    def glite_workflow_requires(self):
        # requirements of the glite workflow, i.e., upload the software stack and the example repo
        # with 2 replicas
        reqs = super(GridWorkflow, self).glite_workflow_requires()

        reqs["software"] = UploadSoftware.req(self, replicas=2)
        reqs["repo"] = UploadRepo.req(self, replicas=2)

        return reqs


class UploadSoftware(Task, law.TransferLocalFile):

    source_path = os.environ["WLCG_EXAMPLE_SOFTWARE"] + ".tgz"

    def single_output(self):
        return self.wlcg_target("software.tgz")

    def run(self):
        # create the local bundle
        bundle = law.LocalFileTarget(self.source_path, is_tmp=True)

        def _filter(tarinfo):
            return None if re.search(r"(\.pyc|\/\.git|\.tgz)$", tarinfo.name) else tarinfo

        bundle.dump(os.path.splitext(self.source_path)[0], filter=_filter)
        self.publish_message("bundled software archive")

        # super().run will upload all files for us
        super(UploadSoftware, self).run()


class UploadRepo(Task, law.BundleGitRepository, law.TransferLocalFile):

    # settings for BundleGitRepository
    repo_path = os.environ["WLCG_EXAMPLE_BASE"]

    # settings for TransferLocalFile
    source_path = None

    task_namespace = None

    def single_output(self):
        path = "{}.{}.tgz".format(os.path.basename(self.repo_path), self.checksum)
        return self.wlcg_target(path, fs="wlcg_fs_software")

    def output(self):
        return law.TransferLocalFile.output(self)

    def run(self):
        bundle = law.LocalFileTarget(is_tmp="tgz")
        self.bundle(bundle)
        self.transfer(bundle)
