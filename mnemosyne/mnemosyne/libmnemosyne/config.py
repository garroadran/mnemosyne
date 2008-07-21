##############################################################################
#
# config.py <Peter.Bienstman@UGent.be>
#
##############################################################################

import md5, random, os, sys, cPickle

from libmnemosyne.exceptions import *



##############################################################################
#
# Config
#
##############################################################################

class Config(Object):

    ##########################################################################
    #
    # __init__
    #
    ##########################################################################

    def __init__(self, basedir=None):

        self._config = {}

        # Set up basedir.

        if basedir == None:

            home = os.path.expanduser("~")

            if sys.platform == "darwin":

                self.old_basedir = os.path.join(home, ".mnemosyne")
                self.basedir = os.path.join(home, "Library", "Mnemosyne")

                if not os.path.exists(self.basedir) \
                   and os.path.exists(self._old_basedir):
                    self.migrate_basedir(self.old_basedir, self.basedir)

            else:

                self.old_basedir = None
                self.basedir = os.path.join(home, ".mnemosyne")

        else:
            
            self.basedir = basedir

        # Load config file from basedir if it exists.

        if os.path.exists(os.path.join(self.basedir, "config")):
            self.load()

        # Set defaults, even if a previous file exists, because we might
        # have added new keys since the last version.

        self.set_defaults()        

        # Load user config file.
        # TODO: check if this still works.

        sys.path.insert(0, self.basedir)

        config_file_c = os.path.join(self.basedir, "config.pyc")
        if os.path.exists(config_file_c):
            os.remove(config_file_c)

        config_file = os.path.join(self.basedir, "config.py")

        if os.path.exists(config_file):
            try:
                import config as user_config
                for var in dir(user_config):
                    if var in config.keys():
                        self._config[var] = getattr(user_config, var))
            except:
                raise ConfigError(stack_trace=True)
            
        # Update paths if the location has migrated.

        if self._old__basedir:

            for key in ['import_dir', 'export_dir', 'import_img_dir',
                        'import_sound_dir']:

                if _config[key] == _old_basedir:
                    _config[key] = self.basedir

        # Recreate user id and log index from history folder in case the
        # config file was accidentally deleted.

        if get_config("log_index") == 1:

            dir = os.listdir(unicode(os.path.join(self.basedir, "history")))
            history_files = [x for x in dir if x[-4:] == ".bz2"]
            history_files.sort()
            if history_files:
                last = history_files[-1]
                user, index = last.split('_')
            index = int(index.split('.')[0])+1

            
        
    ##########################################################################
    #
    # __getitem__
    #
    ##########################################################################

    def __getitem__(self, key):
        
        try:
            return self._config[key]
        except IndexError:
            raise KeyError


        
    ##########################################################################
    #
    # __setitem__
    #
    ##########################################################################

    def __setitem__(self, key, value):
        
        self._config[key] = value



    ##########################################################################
    #
    # set_defaults
    #
    #   TODO: prune unneeded keys.
    #
    ##########################################################################

    def set_defaults(self):

        c = self._config

        c.setdefault("first_run", True)
        c.setdefault("path", "default.mem")
        c.setdefault("import_dir", self.basedir)
        c.setdefault("import_format", "XML")
        c.setdefault("reset_learning_data_import", False)
        c.setdefault("export_dir", self.basedir)
        c.setdefault("export_format", "XML")
        c.setdefault("reset_learning_data_export", False)    
        c.setdefault("import_img_dir", self.basedir)
        c.setdefault("import_sound_dir", self.basedir)    
        c.setdefault("user_id",md5.new(str(random.random())).hexdigest()[0:8])
        c.setdefault("keep_logs", True)
        c.setdefault("upload_logs", True)
        c.setdefault("upload_server", "mnemosyne-proj.dyndns.org:80")    
        c.setdefault("log_index", 1)
        c.setdefault("hide_toolbar", False)
        c.setdefault("QA_font", None)
        c.setdefault("list_font", None)
        c.setdefault("left_align", False)
        c.setdefault("non_latin_font_size_increase", 0)
        c.setdefault("check_duplicates_when_adding", True)
        c.setdefault("allow_duplicates_in_diff_cat", True)
        c.setdefault("grade_0_cards_at_once", 5)
        c.setdefault("randomise_new_cards", False)
        c.setdefault("last_add_vice_versa", False)
        c.setdefault("last_add_category", "<default>")
        c.setdefault("3_sided_input", False) # TODO: remove
        c.setdefault("column_0_width", None)
        c.setdefault("column_1_width", None)
        c.setdefault("column_2_width", None)    
        c.setdefault("sort_column", None)
        c.setdefault("sort_order", None)    
        c.setdefault("show_intervals", "never")
        c.setdefault("only_editable_when_answer_shown", False)
        c.setdefault("locale", None)
        c.setdefault("show_daily_tips", True)
        c.setdefault("tip", 0)
        c.setdefault("backups_to_keep", 5)
        c.setdefault("day_starts_at", 3)

            

    ##########################################################################
    #
    # load
    #
    ##########################################################################

    def load(self):

        try:
            config_file = file(os.path.join(self.basedir, "config"), 'rb')
            for k,v in cPickle.load(config_file).iteritems():
                self._config[k] = v
        except:
            raise ConfigError(stack_trace=True)



    ##########################################################################
    #
    # save
    #
    ##########################################################################

    def save():

        try:
            config_file = file(os.path.join(self.basedir, "config"), 'wb')
            cPickle.dump(self._config, config_file)
        except:
            raise SaveError



    ##########################################################################
    #
    # migrate_basedir
    #
    ##########################################################################

    def migrate_basedir(old, new):

        if os.path.islink(self, _old_basedir):

            print "Not migrating %s to %s because " % (old, new) \
                    + "it is a symlink."
            return

        # Migrate Mnemosyne basedir to new location and create a symlink from 
        # the old one. The other way around is a bad idea, because a user
        # might decide to clean up the old obsolete directory, not realising
        # the new one is a symlink.

        print "Migrating %s to %s" % (old, new)
        try:
            os.rename(old, new)
        except OSError:
            print "Move failed, manual migration required."
            return

        # Now create a symlink for backwards compatibility.

        try:
            os.symlink(new, old)
        except OSError:
            print "Backwards compatibility symlink creation failed."
