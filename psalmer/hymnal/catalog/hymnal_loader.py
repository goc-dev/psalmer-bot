from .hymnal_lib import HymnalLib
import asyncio
import os
import sys
import dulwich.porcelain as git
import dulwich.repo
import dulwich.errors


class HymnalLoader:
    @staticmethod
    async def reload_from_github(i_github_url: str, i_branch: str, i_local_path: str):
        """
        Reload hymnal library from GitHub repository using dulwich (pure Python git).
        - If target directory does not exist or is empty, clone.
        - If target directory is a git repository, pull updates (current branch).
        - If target directory exists but is not a git repository, raise error.
        """
        print(f'Reloading hymnal from {i_github_url} branch {i_branch} into {i_local_path}')

        # Normalize URL (ensure it's a git repository URL)
        repo_url = i_github_url.rstrip('/')

        # Check if directory exists
        if not os.path.exists(i_local_path):
            # Directory does not exist -> clone
            await HymnalLoader._git_clone(repo_url, i_branch, i_local_path)
            return

        # Directory exists, check if it's a git repository
        if not await HymnalLoader._is_git_repo(i_local_path):
            raise RuntimeError(
                f'Directory {i_local_path} exists but is not a git repository. '
                'Cannot reload.'
            )

        # It's a git repo, pull updates (current branch)
        await HymnalLoader._git_pull(i_local_path)

    @staticmethod
    async def _git_clone(repo_url: str, branch: str, target_dir: str):
        """Clone repository into target_dir using dulwich."""
        print(f'Cloning {repo_url} branch {branch} into {target_dir}')
        try:
            # dulwich.porcelain.clone is synchronous; run in thread
            await asyncio.to_thread(
                git.clone,
                repo_url,
                target_dir,
                branch=branch.encode('utf-8'),
                checkout=True
            )
        except Exception as e:
            raise RuntimeError(f'Git clone failed: {e}') from e
        print('Clone finished')

    @staticmethod
    async def _is_git_repo(path: str) -> bool:
        """Check if path is a git repository using dulwich."""
        try:
            # Attempt to open repo; if it fails, it's not a repo
            await asyncio.to_thread(dulwich.repo.Repo, path)
            return True
        except Exception:
            return False

    @staticmethod
    async def _git_pull(repo_path: str):
        """Pull updates for the current branch using dulwich."""
        print(f'Pulling updates for current branch')
        try:
            repo = await asyncio.to_thread(dulwich.repo.Repo, repo_path)
            remote = b'origin'
            # Pull without refspec to use upstream tracking
            await asyncio.to_thread(git.pull, repo, remote)
        except Exception as e:
            raise RuntimeError(f'Git pull failed: {e}') from e
        print('Pull finished')
