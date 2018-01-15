###################################################################
####################  class for plotting data  ####################
###################################################################

import matplotlib
import matplotlib.pyplot as plt
import itertools
import numpy as np
from sklearn.metrics import roc_curve, auc
import math


class PlotData(object):
    """docstring for PlotData"""

    def __init__(self):
        super(PlotData, self).__init__()
        matplotlib.style.use('ggplot')

    def plot_2d(self, x, y, x_label, y_label, title, legend_arr, path_to_save):
        fig = plt.figure()
        plt.clf()
        plt.plot(x)
        plt.plot(y)
        plt.ylabel(y_label)
        plt.xlabel(x_label)
        plt.legend(legend_arr, loc='best')
        plt.title(title)
        plt.savefig(path_to_save)

    def plot_model(self, model_details, path_to_save):
        # Create sub-plots
        plt.clf()
        fig, axs = plt.subplots(1, 2, figsize=(15, 5))
        # Summarize history for accuracy
        axs[0].plot(range(1, len(model_details.history['acc']) + 1),
                    model_details.history['acc'])
        axs[0].plot(range(1, len(model_details.history['val_acc']) + 1),
                    model_details.history['val_acc'])
        axs[0].set_title('Model Accuracy')
        axs[0].set_ylabel('Accuracy')
        axs[0].set_xlabel('Epoch')
        axs[0].set_xticks(np.arange(1, len(model_details.history[
                          'acc']) + 1), len(model_details.history['acc']) / 10)
        axs[0].legend(['train', 'validation'], loc='best')

        # Summarize history for loss
        axs[1].plot(range(1, len(model_details.history['loss']) + 1),
                    model_details.history['loss'])
        axs[1].plot(range(1, len(model_details.history['val_loss']) + 1),
                    model_details.history['val_loss'])
        axs[1].set_title('Model Loss')
        axs[1].set_ylabel('Loss')
        axs[1].set_xlabel('Epoch')
        axs[1].set_xticks(np.arange(1, len(model_details.history[
                          'loss']) + 1), len(model_details.history['loss']) / 10)
        axs[1].legend(['train', 'validation'], loc='best')

        # Save plot
        plt.savefig(path_to_save)

    def plot_model_bis(self, model_details, path_to_save):

        # Create sub-plots
        plt.clf()
        fig, axs = plt.subplots(1, 2, figsize=(15, 5))
        # Summarize history for accuracy
        axs[0].plot(range(1, len(model_details['acc']) + 1),
                    model_details['acc'])
        axs[0].plot(range(1, len(model_details['val_acc']) + 1),
                    model_details['val_acc'])
        axs[0].set_title('Model Accuracy')
        axs[0].set_ylabel('Accuracy')
        axs[0].set_xlabel('Epoch')
        axs[0].set_xticks(np.arange(1, len(model_details[
                          'acc']) + 1), len(model_details['acc']) / 10)
        axs[0].legend(['train', 'validation'], loc='best')

        # Summarize history for loss
        axs[1].plot(range(1, len(model_details['loss']) + 1),
                    model_details['loss'])
        axs[1].plot(range(1, len(model_details['val_loss']) + 1),
                    model_details['val_loss'])
        axs[1].set_title('Model Loss')
        axs[1].set_ylabel('Loss')
        axs[1].set_xlabel('Epoch')
        axs[1].set_xticks(np.arange(1, len(model_details[
                          'loss']) + 1), len(model_details['loss']) / 10)
        axs[1].legend(['train', 'validation'], loc='best')

        # Save plot
        plt.savefig(path_to_save)

    def plot_confusion_matrix(self, cm, classes,
                              path_to_save,
                              normalize=False,
                              title='Confusion matrix',
                              cmap=plt.cm.Blues):
        """
        This function prints and plots the confusion matrix.
        Normalization can be applied by setting `normalize=True`.
        """

        fig = plt.figure()
        plt.clf()
        ax = fig.add_subplot(111)
        ax.set_aspect(1)

        if normalize:
            cm = cm.astype('float') / cm.sum(axis=1)[:, np.newaxis]
            print("Normalized confusion matrix")
        else:
            print('Confusion matrix, without normalization')

        print(cm)

        plt.imshow(cm, interpolation='nearest', cmap=cmap)
        # plt.title(title)
        plt.colorbar()
        tick_marks = np.arange(len(classes))
        plt.xticks(tick_marks, classes)
        plt.yticks(tick_marks, classes)

        fmt = '.2f' if normalize else 'd'
        thresh = cm.max() / 2.
        for i, j in itertools.product(range(cm.shape[0]), range(cm.shape[1])):
            plt.text(j, i, format(cm[i, j], fmt),
                     horizontalalignment="center",
                     verticalalignment='center',
                     fontsize=20,
                     color="white" if cm[i, j] > thresh else "black")
        plt.ylabel('True label')
        plt.xlabel('Predicted label')
        plt.tight_layout()
        ax.grid(False)
        plt.savefig(path_to_save, format='png')

    def plot_roc(self, y_true, y_scores, filename):
        '''
        Plot the ROC for this model.
        '''
        fpr, tpr, thresholds = roc_curve(y_true, y_scores)
        roc_auc = auc(fpr, tpr)
        print('ROC AUC:', roc_auc)
        plt.figure()
        plt.clf()
        plt.plot(fpr, tpr, color='darkorange',
                 label='ROC curve (area = %0.2f)' % roc_auc)
        plt.plot([0, 1], [0, 1], color='navy', linestyle='--')
        plt.xlim([0.0, 1.0])
        plt.ylim([0.0, 1.05])
        plt.xlabel('False Positive Rate')
        plt.ylabel('True Positive Rate')
        plt.title('Receiver operating characteristic curve')
        plt.legend(loc="best")
        plt.savefig(filename)
        plt.close()
        return roc_auc

    def plot_conv_weights(self, weights, filename, input_channel=0):
        plt.figure()
        plt.clf()
        # Get the lowest and highest values for the weights.
        # This is used to correct the colour intensity across
        # the images so they can be compared with each other.
        w_min = np.min(weights)
        w_max = np.max(weights)

        # Number of filters used in the conv. layer.
        num_filters = weights.shape[3]

        # Number of grids to plot.
        # Rounded-up, square-root of the number of filters.
        num_grids = math.ceil(math.sqrt(num_filters))

        # Create figure with a grid of sub-plots.
        fig, axes = plt.subplots(int(num_grids), int(num_grids))

        # Plot all the filter-weights.
        for i, ax in enumerate(axes.flat):
            # Only plot the valid filter-weights.
            if i < num_filters:
                # Get the weights for the i'th filter of the input channel.
                # See new_conv_layer() for details on the format
                # of this 4-dim tensor.
                img = weights[:, :, input_channel, i]

                # Plot image.
                im = ax.imshow(img, vmin=w_min, vmax=w_max,
                               interpolation='nearest')

            # Remove ticks from the plot.
            ax.set_xticks([])
            ax.set_yticks([])

        # Colorbar
        cax, kw = matplotlib.colorbar.make_axes([ax for ax in axes.flat])
        plt.colorbar(im, cax=cax, **kw)
        plt.savefig(filename)
        plt.close()

    def plot_conv_weights(self, weights, filename, input_channel=0):
        plt.figure()
        plt.clf()
        # Get the lowest and highest values for the weights.
        # This is used to correct the colour intensity across
        # the images so they can be compared with each other.
        w_min = np.min(weights)
        w_max = np.max(weights)

        # Number of filters used in the conv. layer.
        num_filters = weights.shape[3]

        # Number of grids to plot.
        # Rounded-up, square-root of the number of filters.
        num_grids = math.ceil(math.sqrt(num_filters))

        # Create figure with a grid of sub-plots.
        fig, axes = plt.subplots(int(num_grids), int(num_grids))

        # Plot all the filter-weights.
        for i, ax in enumerate(axes.flat):
            # Only plot the valid filter-weights.
            if i < num_filters:
                # Get the weights for the i'th filter of the input channel.
                # See new_conv_layer() for details on the format
                # of this 4-dim tensor.
                img = weights[:, :, input_channel, i]

                # Plot image.
                im = ax.imshow(img, vmin=w_min, vmax=w_max,
                               interpolation='nearest')

            # Remove ticks from the plot.
            ax.set_xticks([])
            ax.set_yticks([])

        # Colorbar
        cax, kw = matplotlib.colorbar.make_axes([ax for ax in axes.flat])
        plt.colorbar(im, cax=cax, **kw)
        plt.savefig(filename)
        plt.close()

    def plot_conv_weights_8_4(self, weights, filename, input_channel=0):
        plt.figure()
        plt.clf()
        # Get the lowest and highest values for the weights.
        # This is used to correct the colour intensity across
        # the images so they can be compared with each other.
        w_min = np.min(weights)
        w_max = np.max(weights)

        # Number of filters used in the conv. layer.
        num_filters = weights.shape[3]

        # Create figure with a grid of sub-plots.
        fig, axes = plt.subplots(8, 4)

        # Plot all the filter-weights.
        for i, ax in enumerate(axes.flat):
            # Only plot the valid filter-weights.
            if i < num_filters:
                # Get the weights for the i'th filter of the input channel.
                # See new_conv_layer() for details on the format
                # of this 4-dim tensor.
                img = weights[:, :, input_channel, i]

                # Plot image.
                im = ax.imshow(img, vmin=w_min, vmax=w_max,
                               interpolation='nearest')

            # Remove ticks from the plot.
            ax.set_xticks([])
            ax.set_yticks([])

        # Colorbar
        cax, kw = matplotlib.colorbar.make_axes([ax for ax in axes.flat])
        plt.colorbar(im, cax=cax, **kw)
        plt.savefig(filename)
        plt.close()

    def plot_conv_weights(self, weights, filename, input_channel=0):
        plt.figure()
        plt.clf()
        # Get the lowest and highest values for the weights.
        # This is used to correct the colour intensity across
        # the images so they can be compared with each other.
        w_min = np.min(weights)
        w_max = np.max(weights)

        # Number of filters used in the conv. layer.
        num_filters = weights.shape[3]

        # Number of grids to plot.
        # Rounded-up, square-root of the number of filters.
        num_grids = math.ceil(math.sqrt(num_filters))

        # Create figure with a grid of sub-plots.
        fig, axes = plt.subplots(int(num_grids), int(num_grids))

        # Plot all the filter-weights.
        for i, ax in enumerate(axes.flat):
            # Only plot the valid filter-weights.
            if i < num_filters:
                # Get the weights for the i'th filter of the input channel.
                # See new_conv_layer() for details on the format
                # of this 4-dim tensor.
                img = weights[:, :, input_channel, i]

                # Plot image.
                im = ax.imshow(img, vmin=w_min, vmax=w_max,
                               interpolation='nearest')

            # Remove ticks from the plot.
            ax.set_xticks([])
            ax.set_yticks([])

        # Colorbar
        cax, kw = matplotlib.colorbar.make_axes([ax for ax in axes.flat])
        plt.colorbar(im, cax=cax, **kw)
        plt.savefig(filename)
        plt.close()

    def plot_2d_array(self, arr, filename):
        plt.figure()
        plt.clf()
        plt.imshow(arr)
        plt.axis('off')
        plt.colorbar(orientation='vertical')
        plt.savefig(filename)
        plt.close()

    def plot_conv_output(self, values, filename):
        # Number of filters used in the conv. layer.
        num_filters = values.shape[3]

        # Number of grids to plot.
        # Rounded-up, square-root of the number of filters.
        num_grids = math.ceil(math.sqrt(num_filters))

        # Create figure with a grid of sub-plots.
        fig, axes = plt.subplots(int(num_grids), int(num_grids))

        # Plot the output images of all the filters.
        for i, ax in enumerate(axes.flat):
            # Only plot the images for valid filters.
            if i < num_filters:
                # Get the output image of using the i'th filter.
                img = values[0, :, :, i]

                # Plot image.
                im = ax.imshow(img, interpolation='nearest')

            # Remove ticks from the plot.
            ax.set_xticks([])
            ax.set_yticks([])

        cax, kw = matplotlib.colorbar.make_axes([ax for ax in axes.flat])
        plt.colorbar(im, cax=cax, **kw)
        plt.savefig(filename)
        plt.close()

    def plot_conv_output_8_4(self, values, filename):
        # Number of filters used in the conv. layer.
        num_filters = values.shape[3]

        # Create figure with a grid of sub-plots.
        fig, axes = plt.subplots(8, 4)

        # Plot the output images of all the filters.
        for i, ax in enumerate(axes.flat):
            # Only plot the images for valid filters.
            if i < num_filters:
                # Get the output image of using the i'th filter.
                img = values[0, :, :, i]

                # Plot image.
                im = ax.imshow(img, interpolation='nearest')

            # Remove ticks from the plot.
            ax.set_xticks([])
            ax.set_yticks([])

        cax, kw = matplotlib.colorbar.make_axes([ax for ax in axes.flat])
        plt.colorbar(im, cax=cax, **kw)
        plt.savefig(filename)
        plt.close()