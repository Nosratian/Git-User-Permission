# GitUserPermission - Git user permission for user action
# GitInfo - Git information processing
#
# This program (including classes) processes the data sent through
# the push request based on the committed information to authenticate
# the user for change the branches.
#
# Copyright (c) 2021 by Mahdi Nosratian <Mahdi.Nosratian@gmail.com>
#
# Licensed to MIT License Agreement.
#

import sys
import subprocess
import os
import re
import json
from enum import Enum

class UserAction(Enum):
    CreateBranch = 0
    DeleteBranch = 1
    PushCommits = 2

class GitInfo:
    def __init__(self, base, commit, ref):
        self.base = base
        self.commit = commit
        self.ref = ref
        
    @property
    def base_commit_hash(self):
        return self.base
        
    @property
    def last_commit_hash(self):
        return self.commit

    @property
    def branch_ref_name(self):
        return self.ref

    @property
    def is_new_branch_push(self):
        return re.match(r'[0]{40}', self.base) # if base is all zeros

    @property
    def is_branch_deleted(self):
        return re.match(r'[0]{40}', self.commit) # if commit is all zeros

    @property
    def is_tag(self):
        return self.ref[:9] == "refs/tags"

    @property
    def get_revs(self):
        return self.base + "..." + self.commit
    
    @property
    def get_request_action(self):
        if re.match(r'[0]{40}', self.base):
            return UserAction.CreateBranch
        if re.match(r'[0]{40}', self.commit):
            return UserAction.DeleteBranch
        if not(re.match(r'[0]{40}', self.base) or re.match(r'[0]{40}', self.commit)):  
            return UserAction.PushCommits

    def get_commit_short_id(self, rev):
        result = subprocess.check_output(['git', 'log', '-1', '--pretty=format:%h', rev])
        return result.strip().decode('utf8')

    def get_commit_full_id(self, rev):
        result = subprocess.check_output(['git', 'log', '-1', '--pretty=format:%H', rev])
        return result.strip().decode('utf8')
        
    def get_auther_name(self, rev):
        result = subprocess.check_output(['git', 'log', '-1', '--pretty=format:%an', rev])
        return result.strip().decode('utf8')
        
    def get_auther_email(self, rev):
        result = subprocess.check_output(['git', 'log', '-1', '--pretty=format:%ae', rev])
        return result.strip().decode('utf8')

    def get_committer_name(self, rev):
        result = subprocess.check_output(['git', 'log', '-1', '--pretty=format:%cn', rev])
        return result.strip().decode('utf8')

    def get_committer_email(self, rev):
        result = subprocess.check_output(['git', 'log', '-1', '--pretty=format:%ce', rev])
        return result.strip().decode('utf8')

    def get_branch_name(self, rev):
        result = self.ref.replace("refs/heads/", "").replace("refs/tags/", "").replace("refs/remotes/", "")
        return result

class GitUserPermission:
    def __init__(self, user, branch):
        self.user = user
        self.branch = branch

    @property
    def user_role(self):
        return self.__get_user_role()
        
    def __get_user_role(self):
        user_file = "./hooks/users.json"
        with open(user_file) as file:
            data = json.load(file)
            
        user_access = list(filter(lambda x: x["UserName"] == self.user, data["UsersInfo"]))
        
        if user_access:
            branch_access = list(filter(lambda x: x["Branch"] == self.branch, user_access[0]["AccessList"]))
            if not branch_access:
                branch_star_list = list(filter(lambda x: x["Branch"].endswith("*"), user_access[0]["AccessList"]))
                for branch_star in branch_star_list:
                    branch_name = branch_star["Branch"]
                    start_star = branch_name.find("*")
                    branch_without_star = branch_name[:start_star]
                    if self.branch.startswith(branch_without_star):
                        return branch_star["Role"]
        else:
            return ""

        if branch_access:
            return branch_access[0]["Role"]
        else:
            return ""

def is_user_permission(gitInfo):
    try:
        action = gitInfo.get_request_action        
        revs = gitInfo.get_revs
        
        if gitInfo.is_new_branch_push:
            revs = gitInfo.last_commit_hash
        
        if gitInfo.is_branch_deleted:
            revs = gitInfo.base_commit_hash

        proc = subprocess.Popen(['git', 'rev-list', '--oneline', '--first-parent', revs], stdout=subprocess.PIPE)
        lines = proc.stdout.readlines()
        if lines:
            last_line = lines[0]
            rev = last_line.strip().decode('utf8').split()[0]
            user_name = gitInfo.get_committer_name(rev)
            branch_name = gitInfo.get_branch_name(rev)
            gitUserPermission = GitUserPermission(user_name, branch_name)
            role = gitUserPermission.user_role
        
            if gitInfo.is_tag: # skip tags
                return False
                
            if action == UserAction.CreateBranch and (role.lower() == "create" or role.lower() == "admin"):
                return True

            if action == UserAction.DeleteBranch and (role.lower() == "delete" or role.lower() == "admin"):
                return True

            if action == UserAction.PushCommits and (role.lower() == "write" or role.lower() == "admin"):
                return True

            return False
        else:
            return False
        
    except Exception:
        return False
            
    return False
                
def main():
    result = ""
    ref = sys.argv[1]
    base = sys.argv[2]
    commit = sys.argv[3]
    gitInfo = GitInfo(base, commit, ref)
    user_permission = is_user_permission(gitInfo)
    
    if user_permission:
        result = "User Ok"
        sys.exit(0)
    else:
        result = "User Not Permission"
        sys.exit(1)
 
if __name__ == "__main__":
    main()
